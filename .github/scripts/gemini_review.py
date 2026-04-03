import os, json, urllib.request, urllib.error, subprocess, sys, re

key = os.environ["GEMINI_API_KEY"]
pr  = os.environ["PR_NUMBER"]

def pick_model():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    data = json.loads(urllib.request.urlopen(url).read())
    prefer = ["gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-2.5-pro", "gemini-2.0-flash"]
    available = {m["name"].split("/")[-1] for m in data.get("models", [])
                 if "generateContent" in m.get("supportedGenerationMethods", [])}
    for name in prefer:
        if name in available:
            return name
    for m in data.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            return m["name"].split("/")[-1]
    raise RuntimeError(f"No usable model found. Available: {available}")

model = pick_model()
print(f"Using model: {model}")

diff = open("diff.txt").read() or "(empty diff)"

prompt = (
    "你是一位资深前端工程师，专注于游戏平台开发（React/TypeScript/SolidJS）。\n"
    "请对以下 PR diff 进行 Code Review。\n"
    "评分时额外关注：游戏状态更新的竞态风险、动画帧回调内存泄漏、用户输入未校验（XSS）。\n\n"
    "严格按照以下格式输出，每行一条，不要输出其他内容：\n"
    "SCORE|功能正确性|<0-10分>|<一句话说明>\n"
    "SCORE|代码质量|<0-10分>|<一句话说明>\n"
    "SCORE|性能|<0-10分>|<一句话说明>\n"
    "SCORE|安全性|<0-10分>|<一句话说明>\n"
    "SCORE|可维护性|<0-10分>|<一句话说明>\n"
    "TOTAL|<五项总分>\n"
    "COMMENT|<2-3句综合建议，中文>\n\n"
    "Diff:\n" + diff
)

payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

try:
    resp = json.loads(urllib.request.urlopen(req).read())
except urllib.error.HTTPError as e:
    print(f"Gemini API error {e.code}: {e.read().decode()}", file=sys.stderr)
    sys.exit(1)

raw = resp["candidates"][0]["content"]["parts"][0]["text"]
print(raw)

# 解析结构化输出
ICONS = {"功能正确性": "🎯", "代码质量": "🧹", "性能": "⚡", "安全性": "🔒", "可维护性": "🔧"}

def badge(score):
    color = "brightgreen" if score >= 9 else ("yellow" if score >= 7 else "red")
    return f"![{score}/10](https://img.shields.io/badge/{score}%2F10-{color}?style=flat-square)"

rows = []
total = 0
comment = ""

for line in raw.splitlines():
    line = line.strip()
    if line.startswith("SCORE|"):
        parts = line.split("|", 3)
        if len(parts) == 4:
            _, dim, score_str, desc = parts
            try:
                score = int(score_str)
            except ValueError:
                score = 0
            icon = ICONS.get(dim, "📌")
            rows.append(f"| {icon} **{dim}** | {badge(score)} | {desc} |")
    elif line.startswith("TOTAL|"):
        try:
            total = int(line.split("|", 1)[1])
        except (ValueError, IndexError):
            pass
    elif line.startswith("COMMENT|"):
        comment = line.split("|", 1)[1] if "|" in line else ""

passed = total >= 40
verdict_icon = "✅" if passed else "❌"
verdict_text = "建议合并" if passed else "建议修改后再合并"

# 如果解析失败（Gemini 没按格式输出），降级为原始文本
if not rows:
    m = re.search(r"TOTAL:\s*(\d+)", raw)
    total = int(m.group(1)) if m else 0
    body = f"## 🤖 AI Code Review\n\n{verdict_icon} **总分 {total} / 50 — {verdict_text}**\n\n---\n\n{raw}\n\n"
else:
    table = (
        "| 维度 | 评分 | 说明 |\n"
        "|------|------|------|\n" +
        "\n".join(rows)
    )
    body = (
        f"## 🤖 AI Code Review\n\n"
        f"{verdict_icon} **总分 {total} / 50 — {verdict_text}**\n\n"
        + (f"> 💬 {comment}\n\n" if comment else "")
        + f"<details>\n<summary>📋 查看评分详情</summary>\n\n{table}\n\n</details>\n\n"
        + f"<sub>由 {model} 自动生成 · 不替代人工 Review 和 CI 检查</sub>"
    )

open("review_body.md", "w").write(body)
subprocess.run(["gh", "pr", "comment", pr, "--body-file", "review_body.md"], check=True)


# 自动打标签
repo = os.environ.get("GITHUB_REPOSITORY", "")
if total >= 45:
    label, color, desc = "ai-approved", "0075ca", "AI 评分优秀 ≥45"
elif total >= 40:
    label, color, desc = "ai-low-risk", "cfd3d7", "AI 评分良好 40-44"
elif total >= 35:
    label, color, desc = "ai-medium-risk", "e4e669", "AI 评分一般 35-39"
else:
    label, color, desc = "ai-high-risk", "d93f0b", "AI 评分较低 <35"

# 确保 label 存在
subprocess.run(["gh", "label", "create", label, "--color", color, "--description", desc, "--repo", repo, "--force"],
               capture_output=True)
subprocess.run(["gh", "pr", "edit", pr, "--add-label", label, "--repo", repo], check=True)

sys.exit(0 if passed else 1)
