import os, json, urllib.request, urllib.error, subprocess, sys, re

key = os.environ["GEMINI_API_KEY"]
pr  = os.environ["PR_NUMBER"]

# 自动发现可用模型（优先快速模型）
def pick_model():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    data = json.loads(urllib.request.urlopen(url).read())
    prefer = ["gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-2.5-pro", "gemini-2.0-flash"]
    available = {m["name"].split("/")[-1] for m in data.get("models", [])
                 if "generateContent" in m.get("supportedGenerationMethods", [])}
    for name in prefer:
        if name in available:
            return name
    # 兜底：取第一个支持 generateContent 的
    for m in data.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            return m["name"].split("/")[-1]
    raise RuntimeError(f"No usable model found. Available: {available}")

model = pick_model()
print(f"Using model: {model}")

diff = open("diff.txt").read() or "(empty diff)"

prompt = (
    "你是一位资深前端工程师，请对以下 PR diff 进行 Code Review。\n\n"
    "按五个维度各给 0-10 分：\n"
    "1. 功能正确性（逻辑是否正确，有无明显 bug）\n"
    "2. 代码质量（可读性、命名、结构）\n"
    "3. 性能（有无不必要的重渲染、大循环等）\n"
    "4. 安全性（有无 XSS、数据泄露等风险）\n"
    "5. 可维护性（是否易于后续修改）\n\n"
    "输出格式（严格遵守）：\n"
    "先输出五行评分，每行格式：维度名：X/10 - 简短说明\n"
    "然后输出一行总分：TOTAL: XX/50（XX 为五项之和，这行必须存在）\n"
    "最后输出综合建议（2-3 句话，中文）。\n\n"
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

review = resp["candidates"][0]["content"]["parts"][0]["text"]

m = re.search(r"TOTAL:\s*(\d+)", review)
total = int(m.group(1)) if m else 0
passed = total >= 35
verdict = f"{'✅' if passed else '❌'} 评分 {total}/50，{'建议合并' if passed else '建议修改后再合并'}"

body = (
    f"## AI Code Review（{model}）\n\n"
    f"{review}\n\n"
    f"---\n**{verdict}**\n*由 Gemini 自动生成 · 不替代 CI 检查*"
)
open("review_body.md", "w").write(body)
subprocess.run(["gh", "pr", "comment", pr, "--body-file", "review_body.md"], check=True)
sys.exit(0 if passed else 1)
