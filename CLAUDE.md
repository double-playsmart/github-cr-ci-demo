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
    claude-review.yml         # 可选：Claude Code PR 自动 review（需配置 ANTHROPIC_API_KEY）
  ISSUE_TEMPLATE/             # Bug report / Feature request 模板
  pull_request_template.md    # PR 填写模板
docs/                         # 面向 AI 的文档：demo 脚本、设置清单、路线图
```

## CI 流程

`.github/workflows/ci.yml` 运行于 ubuntu-latest + Node 20，触发条件：
- push 到 `main`、`master`、`feature/**`
- 所有 Pull Request

步骤：checkout → 安装 Node → `npm ci` → `npm run lint` → `npm run build`

## Claude PR Review（可选）

`.github/workflows/claude-review.yml` 在 PR 打开/更新时触发 AI 自动 review。需在仓库 Secrets 中配置 `ANTHROPIC_API_KEY`。详见 `docs/claude-review-setup.md`。

## 分支与 PR 规范

- 分支命名：`feature/*`、`fix/*`、`docs/*`
- PR 要小且聚焦，使用 `.github/pull_request_template.md` 模板
- 推送前本地跑 `npm run check`
- `main` 分支受保护：需 ≥1 人 approve + CI 通过

## 项目定位

这是一个用于演示 GitHub Code Review 与 CI 流程的教学示例项目。改动应保持最小化、流程可见。进阶计划见 `docs/roadmap.md`（当前处于 Level 1）。
