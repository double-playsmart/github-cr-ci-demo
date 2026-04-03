# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指引。

## 常用命令

```bash
npm run dev      # 启动 Vite 开发服务器（http://localhost:5173）
npm run lint     # 运行 ESLint
npm run build    # Vite 生产构建（输出到 dist/）
npm run check    # 完整校验：lint + build（推送前必跑）
```

暂无测试框架，验证门槛为 lint + build。

## 架构概览

纯原生 JS 静态站点，无框架、无运行时依赖。构建工具：Vite；代码检查：ESLint v9 flat config。

```
index.html                    # 入口，以 ES module 方式加载 src/main.js
src/main.js                   # 通过模板字符串注入硬编码的 demo 卡片内容
src/style.css                 # CSS Grid 布局、渐变、backdrop-filter
.github/
  workflows/
    ci.yml                    # CI：在 push/PR 时跑 lint + build
    claude-review.yml         # AI PR Review：当前实际跑 Gemini（见下方说明）
  scripts/
    gemini_review.py          # Gemini review 实现：读 diff → 调 API → 贴 PR 评论，总分 <35/50 则 workflow 失败
  pull_request_template.md    # PR 填写模板
docs/
    指南.md                   # 完整技术文档（原理 + 配置）
    demo-script.md            # 演示脚本（含坏代码速查）
    汇报总结.md               # 面向团队的汇报材料
    roadmap.md                # 四级进阶路线图
```

## CI 流程（ci.yml）

运行于 ubuntu-latest + Node 20，触发：push 到 `main`/`master`/`feature/**` 及所有 PR。

步骤：checkout → `npm ci` → `npm run lint` → `npm run build`

## AI PR Review（claude-review.yml + gemini_review.py）

PR 打开/更新时触发，**当前实际运行 Gemini**（需配置 Secret `GEMINI_API_KEY`）。

执行路径：
1. workflow 用 `git diff` 生成 `diff.txt`
2. 调用 `scripts/gemini_review.py`：自动选可用 Gemini 模型 → 对 diff 按五维度（功能正确性/代码质量/性能/安全性/可维护性）各评 0-10 分 → 用 `gh pr comment` 贴到 PR 评论
3. 总分 ≥ 35/50 → exit 0（通过），< 35 → exit 1（workflow 失败）

**切换到 Claude**：Secrets 加 `ANTHROPIC_API_KEY`，注释掉 `gemini-review` job，取消注释 `claude-review` job。详见 `docs/claude-review-setup.md`。

## GitHub 协作配置

- `pull_request_template.md`：开 PR 时自动填充描述模板
- `CODEOWNERS`：指定代码 owner，PR 自动 request review

## 分支与 PR 规范

- 分支命名：`feature/*`、`fix/*`、`docs/*`
- PR 要小且聚焦，使用 `.github/pull_request_template.md` 模板
- 推送前本地跑 `npm run check`
- `main` 分支受保护：需 ≥1 人 approve + CI 通过

## 项目定位

这是一个用于演示 GitHub Code Review 与 CI 流程的教学示例项目。改动应保持最小化、流程可见。进阶计划见 `docs/roadmap.md`（当前处于 Level 1）。
