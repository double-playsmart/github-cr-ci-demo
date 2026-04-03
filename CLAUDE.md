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
  ISSUE_TEMPLATE/             # GitHub Issue 结构化表单模板（bug report / feature request）
  pull_request_template.md    # PR 填写模板
docs/                         # 面向 AI 的文档：demo 脚本、设置清单、路线图
```

## CI 流程

`.github/workflows/ci.yml` 运行于 ubuntu-latest + Node 20，触发条件：
- push 到 `main`、`master`、`feature/**`
- 所有 Pull Request

步骤：checkout → 安装 Node → `npm ci` → `npm run lint` → `npm run build`

## AI PR Review

`.github/workflows/claude-review.yml` 在 PR 打开/更新时触发，**当前实际运行 Gemini**（需配置 Secret `GEMINI_API_KEY`）。

执行路径：workflow 生成 `diff.txt` → 调用 `scripts/gemini_review.py` → 脚本用 Gemini API 对 diff 按五维度（功能正确性/代码质量/性能/安全性/可维护性）各评 0-10 分，总分 ≥ 35/50 通过，< 35 则 workflow 失败。评审结果自动贴到 PR 评论。

**切换到 Claude**：在仓库 Secrets 加 `ANTHROPIC_API_KEY`，注释掉 workflow 中的 `gemini-review` job，取消注释 `claude-review` job 即可。详见 `docs/claude-review-setup.md`。

## 分支与 PR 规范

- 分支命名：`feature/*`、`fix/*`、`docs/*`
- PR 要小且聚焦，使用 `.github/pull_request_template.md` 模板
- 推送前本地跑 `npm run check`
- `main` 分支受保护：需 ≥1 人 approve + CI 通过

## 项目定位

这是一个用于演示 GitHub Code Review 与 CI 流程的教学示例项目。改动应保持最小化、流程可见。进阶计划见 `docs/roadmap.md`（当前处于 Level 1）。
