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
    ci.yml              ← 构建质量门禁
    claude-review.yml   ← AI Review 入口
  scripts/
    gemini_review.py    ← AI Review 实现
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
- Gemini 评论出现，五维打分 ≥ 40/50，显示「✅ 建议合并」

---

### 第三步：演示"坏代码"PR（3 分钟，重点）

```bash
git checkout -b demo/bad-change
```

把以下代码粘贴进 `src/main.js` 底部：

```js
// 故意写烂的函数：命名混乱 + XSS 风险
function a(x) {
  var d = document.getElementById('app')
  d.innerHTML = x   // 直接注入，XSS 风险
  var arr = []
  for (var i=0;i<10000;i++) { arr.push(i*i*i) }  // 无意义大循环
  return arr
}
```

```bash
git add src/main.js
git commit -m "fix: temp"
git push -u origin demo/bad-change
```

去 GitHub 开 PR，等结果：
- CI 可能通过（lint 不一定能抓住逻辑问题）
- **Gemini 给出低分 + 指出 XSS 风险和命名问题，显示「❌ 建议修改后再合并」**

这里的核心观点：**CI 管跑不跑得起来，AI Review 管写得好不好，两者互补。**

---

### 第四步：说明可切换模型（1 分钟）

打开 `.github/workflows/claude-review.yml`，展示底部注释的 Claude job：

> 现在跑的是 Gemini（免费），团队内部可以切换到 Claude，改两行配置就行。
> 两个模型用的是同一套五维评分 prompt，结果可以直接对比。

---

### 第五步：说明强制门禁（1 分钟）

打开 GitHub 仓库 → Settings → Branches，指向 `main` 的 protection rules：

- Require CI 通过（validate job）
- Require ≥1 人 Approve
- 如果把 AI Review job 也加进 required checks → **AI 打低分可以直接阻断 merge**

> 这不是可选的建议，是强制的流程门禁。

---

## 坏代码速查（现场直接复制）

```js
function a(x) {
  var d = document.getElementById('app')
  d.innerHTML = x
  var arr = []
  for (var i=0;i<10000;i++) { arr.push(i*i*i) }
  return arr
}
```

问题点（让 AI 帮你发现）：
- `a` / `x` / `d`：命名完全无意义
- `d.innerHTML = x`：XSS 注入风险
- 无意义的 10000 次循环：性能问题
- `var` 而不是 `const/let`：代码质量

---

## 演示前检查清单

- [ ] `GEMINI_API_KEY` 已配置在 GitHub Secrets
- [ ] branch protection 已开启（CI required）
- [ ] 本地 `npm run check` 通过
- [ ] 已有一个干净的 `main` 分支
