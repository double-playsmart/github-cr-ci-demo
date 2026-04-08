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
    pr-agent.yml              # ★ AI PR Review：PR-Agent 开源方案（当前使用）
  pull_request_template.md    # PR 填写模板
.pr_agent.toml                # ★ PR-Agent 配置：审查规则、模型、中文输出
docs/
    指南.md                   # 完整技术文档（原理 + 配置）
    汇报总结.md               # 面向团队的汇报材料
    migration-guide.md        # CR/CI 流程迁移指南
```

## CI 流程（ci.yml）

运行于 ubuntu-latest + Node 20，触发：push 到 `main`/`master`/`feature/**` 及所有 PR。

步骤：checkout → `npm ci` → `npm run lint` → `npm run build`

## AI PR Review（pr-agent.yml + .pr_agent.toml）

PR 打开/更新时触发，使用 **PR-Agent 开源方案**（需配置 Secret `GEMINI_API_KEY`）。

执行路径：
1. PR 打开 → `pr-agent.yml` 触发 `qodo-ai/pr-agent@main`
2. 读取 `.pr_agent.toml` 中的配置和 `extra_instructions` 审查规则
3. 调用 Gemini API → 自动生成 PR 描述 + 中文 review 评论（区分必须修改/建议优化）
4. 支持 PR 评论命令：`/review` `/describe` `/improve` `/ask 问题`

**切换 AI**：编辑 `pr-agent.yml`，注释/取消注释对应的 MODEL 和 KEY 两行即可切换 Claude/GPT。详见 `docs/指南.md`。

## GitHub 协作配置

- `pull_request_template.md`：开 PR 时自动填充描述模板
- `CODEOWNERS`：指定代码 owner，PR 自动 request review

## 分支与 PR 规范

- 分支命名：`feature/*`、`fix/*`、`docs/*`
- PR 要小且聚焦，使用 `.github/pull_request_template.md` 模板
- 推送前本地跑 `npm run check`
- `main` 分支受保护：需 ≥1 人 approve + CI 通过

## 项目定位

这是一个用于演示 GitHub Code Review 与 CI 流程的教学示例项目。改动应保持最小化、流程可见。迁移指南见 `docs/migration-guide.md`。
