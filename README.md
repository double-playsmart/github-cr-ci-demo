# GitHub CR / CI Demo

一个最小前端演示仓库，用于展示 GitHub Code Review 和 CI 的完整协作流程。

前端代码故意保持最简，重点在链路：

```
本地改代码 → push → CI 自动检查 → 提 PR → AI 自动 Review → 人工 Review → merge
```

**[完整中文指南 → docs/指南.md](docs/指南.md)**

---

## 快速开始

```bash
npm install
npm run check    # 本地验证（等价于 CI 跑的内容）
npm run dev      # 启动开发服务器
```

## 核心配置文件

| 文件 | 作用 |
|------|------|
| `.github/workflows/ci.yml` | CI：push/PR 时自动跑 lint + build |
| `.github/workflows/claude-review.yml` | AI Review：PR 时 Gemini 自动打分（Claude 预留） |
| `.github/pull_request_template.md` | PR 模板：含前端五维打分表 |
| `docs/指南.md` | 中文主文档：原理、配置、演示流程 |

## GitHub 仓库设置

```
Settings → Branches → main → 开启 branch protection：
✅ Require pull request before merging（至少 1 approval）
✅ Require status checks（添加 "validate"）
✅ Require conversation resolution
```

详见 [docs/指南.md](docs/指南.md)
