# 演示脚本

## 核心流程（一句话）

```
改代码 → push → PR → CI 自动检查 + AI 自动 Review → 人工 Approve → merge
```

---

## 演示路径（约 10 分钟）

### 第一步：介绍仓库结构（1 分钟）

打开 `docs/指南.md`，展示目录结构，重点指出：

```
.github/
  workflows/
    ci.yml              ← 构建质量门禁（lint + build + reviewdog）
    pr-agent.yml        ← AI Review 入口（PR-Agent 开源方案）
.pr_agent.toml          ← AI 审查规则配置
```

一句话：**左边管代码能不能跑，右边管代码写得好不好。**

---

### 第二步：演示"好代码"PR（3 分钟）

```bash
git checkout main && git pull
git checkout -b demo/good-change
```

在 `src/main.js` 改一行正常文案，然后：

```bash
npm run check   # 本地验证通过
git add src/main.js
git commit -m "feat: update card title"
git push -u origin demo/good-change
```

去 GitHub 开 PR，等约 30 秒，展示：
- CI 绿色通过
- PR-Agent 自动生成 PR 描述（类型 + 改动说明 + 文件列表）
- PR-Agent 发出中文 Review 评论，无严重问题

---

### 第三步：演示"坏代码"PR（3 分钟，重点）

```bash
git checkout main && git pull
git checkout -b demo/bad-change
```

`src/main.js` 已包含坏代码示例（XSS + 大循环 + 单字母命名）。

去 GitHub 开 PR，等结果：
- CI 通过（lint 不一定能抓住逻辑问题）
- **PR-Agent 指出 XSS 风险、大循环性能问题和命名问题**

这里的核心观点：**CI 管跑不跑得起来，AI Review 管写得好不好，两者互补。**

---

### 第四步：演示交互命令（2 分钟）

在 PR 评论区输入命令演示：

| 命令 | 演示效果 |
|------|---------|
| `/improve` | AI 给出具体修复代码（含可 commit 的 diff） |
| `/ask XSS 怎么修` | AI 针对这个 PR 回答问题 |
| `/review` | 手动重新触发 review |

---

### 第五步：说明可切换模型（1 分钟）

打开 `.github/workflows/pr-agent.yml`，展示注释的模型配置：

> 现在跑的是 Gemini（免费 1000 次/天），团队内部可以切换到 Claude 或 GPT，注释两行取消注释两行就行。
> 审查规则在 `.pr_agent.toml` 里，跟模型无关，换模型不用改规则。

---

### 第六步：说明强制门禁（1 分钟）

打开 GitHub 仓库 → Settings → Rules → Rulesets，指向 `main` 的保护规则：

- Require CI 通过（validate job）
- Require ≥1 人 Approve
- AI Review 只做参考，不阻断（靠人判断是否采纳 AI 建议）

> CI + 人工 Approve 是硬门禁，AI Review 是辅助信息。

---

## 坏代码速查（现场直接复制）

```js
// ❌ 问题1：直接 innerHTML 注入用户输入，XSS 风险
const u = location.search; // 单字母命名，含义不明
app.innerHTML = `<div class="user-info">${u}</div>`; // 未经转义直接注入

// ❌ 问题2：无意义大循环，阻塞主线程
for (let i = 0; i < 100000; i++) {
  // 空循环，无实际业务意义
}
```

问题点（让 AI 帮你发现）：
- `u`：单字母命名，含义不明
- `innerHTML = location.search`：XSS 注入风险
- 无意义的 100000 次循环：性能问题

---

## 演示前检查清单

- [ ] `GEMINI_API_KEY` 已配置在 GitHub Secrets
- [ ] Rulesets 已开启（CI required + 1 approval）
- [ ] 本地 `npm run check` 通过
- [ ] 已有一个干净的 `main` 分支
