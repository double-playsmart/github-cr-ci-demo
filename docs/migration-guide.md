# CR / CI 流程迁移指南

> 目标：将本仓库验证过的 Code Review + CI + AI Review 流程，快速复制到团队的其他 GitHub 仓库。
>
> 本文档面向 Claude / AI 协作者和团队成员，提供完整上下文和逐步操作。

---

## 一、流程架构

```
开发者本地
  │
  ├─ git checkout -b feature/xxx
  ├─ 改代码 → pnpm run check（本地验证）
  └─ git push → 提 Pull Request
         │
         ▼
    GitHub 收到 PR
         │
         ├─ CI（ci.yml）
         │   ├─ pnpm install
         │   ├─ pnpm tsc --noEmit        # 类型检查
         │   ├─ pnpm lint                 # ESLint
         │   ├─ reviewdog                 # ESLint 错误 → PR inline comment
         │   └─ pnpm build               # 构建
         │
         ├─ AI Review（pr-agent.yml）
         │   ├─ 读取 .pr_agent.toml 配置和审查规则
         │   ├─ 自动生成 PR 描述（类型 + 文件列表）
         │   ├─ 自动发中文 Review 评论
         │   │   ├─ 精力评估（1-5）
         │   │   ├─ 安全问题分析
         │   │   ├─ 重点审查项（链接到代码行）
         │   │   └─ 是否建议拆分 PR
         │   └─ 自动打标签（PR 类型 / effort / security）
         │
         ├─ Reviewer 人工 review + Approve
         │
         └─ CI 通过 + ≥1 人 Approve → 可以 Merge
```

**关键设计决策：**
- CI（lint / type check / build）是硬门禁，失败阻断合并
- AI Review 只发评论和标签，不阻断（开源版 PR-Agent 无此能力，且 AI 误判率不低）
- `skip-ai-review` 标签可跳过 AI Review（批量翻译 / 配置类 PR）

---

## 二、需要复制的文件清单

```
目标仓库/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  # CI 流程（需按项目调整）
│   │   └── pr-agent.yml            # AI Review（直接复制）
│   ├── pull_request_template.md    # PR 模板（按团队调整）
│   └── CODEOWNERS                  # 代码负责人（按团队填写）
├── .pr_agent.toml                  # AI 审查规则（直接复制，微调 extra_instructions）
└── CLAUDE.md                       # Claude Code 工作指引（按项目编写）
```

---

## 三、逐步操作

### Step 1：配置 GitHub Secret

在目标仓库 → Settings → Secrets and variables → Actions → New repository secret：

| Secret 名 | 来源 | 说明 |
|-----------|------|------|
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com/apikey) | 免费，1000 次/天（flash-lite） |

切换 Claude 时另加 `ANTHROPIC_API_KEY`（[console.anthropic.com](https://console.anthropic.com/)，约 ¥0.1/次）。

### Step 2：复制 pr-agent.yml

```yaml
# .github/workflows/pr-agent.yml
name: PR Agent

on:
  pull_request:
    types: [opened, reopened, ready_for_review]
  issue_comment:

jobs:
  pr_agent:
    if: ${{ github.event.sender.type != 'Bot' && !contains(github.event.pull_request.labels.*.name, 'skip-ai-review') }}
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
      contents: read
    steps:
      - uses: qodo-ai/pr-agent@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

          # ── 当前使用 Gemini（免费） ──
          CONFIG.MODEL: "gemini/gemini-2.5-flash-lite"
          GOOGLE_AI_STUDIO.GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}

          # ── 切换 Claude 时：注释上面两行，取消注释下面两行 ──
          # CONFIG.MODEL: "anthropic/claude-sonnet-4-6"
          # ANTHROPIC.KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**直接复制，无需修改。** 切换模型只改注释。

### Step 3：复制 .pr_agent.toml

```toml
# .pr_agent.toml
# 修改后 push 即生效

[config]
response_language = "zh-CN"
fallback_models = []
custom_model_max_tokens = 1048576
ignore_pr_labels = ["skip-ai-review"]

[github_action_config]
auto_review = true
auto_describe = true
auto_improve = false

[pr_reviewer]
require_estimate_effort_to_review = true
require_tests_review = true               # ← 有测试框架时开启
require_security_review = true
require_ticket_analysis_review = false
require_can_be_split_review = true
enable_review_labels_effort = true
enable_review_labels_security = true
enable_help_text = false

# ✏️ 按项目定制审查规则
extra_instructions = """
你是一位资深前端工程师，专注于游戏平台开发（React/TypeScript/SolidJS）。
审查时重点关注以下规则：

【安全性】
- 禁止将用户输入直接赋值给 innerHTML/outerHTML，防止 XSS 注入
- 敏感信息（API Key、Token）不得出现在代码中

【性能】
- 避免在循环内进行 DOM 操作或重复调用高开销函数
- 避免无意义的大循环（超过 10000 次且无实际业务意义）
- 事件监听器和定时器必须在组件卸载时清理，防止内存泄漏

【代码质量】
- 变量、函数命名必须有实际含义，禁止单字母命名（循环变量 i/j/k 除外）
- 使用 const/let，禁止使用 var

【游戏业务专项】
- 涉及赔率、金额的数值计算，检查浮点精度问题
- WebSocket 消息处理必须考虑竞态条件，避免旧消息覆盖新状态
- 游戏状态变更必须通过统一入口，禁止直接修改状态对象
- FSM 状态转换逻辑是否完整，有无遗漏的状态分支
- Provider 接口变更是否向后兼容

输出要求：
- 语言：中文
- 区分「必须修改」和「建议优化」并明确标注
- 指出问题时同时给出修改建议
"""

[pr_description]
publish_labels = true
use_bullet_points = true
keep_original_user_description = true
include_generated_by_header = false

[pr_code_suggestions]
num_code_suggestions = 4
focus_only_on_problems = true
suggestions_score_threshold = 5

[ignore]
glob = [
  "*.lock",
  "dist/**",
  "node_modules/**",
  "*.min.js",
  "*.min.css",
  "src/locales/**",
  "src/i18n/**",
]
```

**需要按项目调整的部分：**
- `extra_instructions`：补充项目特有的审查规则
- `require_tests_review`：有测试框架时设为 `true`
- `[ignore] glob`：加入项目特有的生成文件目录（如 `src/locales/**`）

### Step 4：编写 ci.yml（按项目调整）

pnpm + TypeScript 项目示例：

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, master, "feature/**"]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - name: Type Check
        run: pnpm tsc --noEmit

      - name: Lint
        run: pnpm lint

      - name: Lint inline comments (PR only)
        if: github.event_name == 'pull_request'
        uses: reviewdog/action-eslint@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          reporter: github-pr-review
          eslint_flags: "src/"
          fail_on_error: false

      - name: Build
        run: pnpm build
```

**按项目调整：**
- 包管理器：`npm ci` → `pnpm install --frozen-lockfile`
- 加入 `pnpm tsc --noEmit`（游戏组高频类型错误）
- `eslint_flags` 指向实际源码目录
- monorepo 可能需要加 `--filter` 参数

### Step 5：创建 PR 模板

```markdown
<!-- .github/pull_request_template.md -->
## 交付 Checklist

请逐项勾选并补充必要信息。

- [ ] **JIRA**：在评论中附上 JIRA 链接（无关联工单时在评论中说明原因）
- [ ] **线上自测**：核心业务流生产环境自测通过
- [ ] **通知测试**：通知测试验收（无测试则 @前端）
- [ ] **通知后端**：通知测试验收（无后端则 @前端）
- [ ] **通知产品**：通知产品验收（无产品则 @前端）
- [ ] **验收完成**：产品 / 测试 / 前端均已确认
```

### Step 6：配置 GitHub Rulesets

目标仓库 → Settings → Rules → Rulesets → New branch ruleset：

| 设置 | 值 |
|------|------|
| Name | `main protection` |
| Enforcement | Active |
| Target | Default branch |
| Require pull request | ✅（Required approvals: 1） |
| Require status checks | ✅（添加 `validate`） |
| Block force pushes | ✅ |

注意：`validate` 需要至少跑过一次才能被搜索到。先提一个 PR 让 CI 跑完再配置。

### Step 7：创建 skip 标签

```bash
gh label create "skip-ai-review" --color "ededed" --description "跳过 AI Review（批量翻译/配置类 PR）"
```

---

## 四、配置速查表

### .pr_agent.toml 完整配置项说明

| Section | 配置项 | 当前值 | 说明 |
|---------|--------|--------|------|
| `[config]` | `response_language` | `"zh-CN"` | 输出语言 |
| | `fallback_models` | `[]` | 禁用自动切换模型 |
| | `custom_model_max_tokens` | `1048576` | flash-lite context window |
| | `ignore_pr_labels` | `["skip-ai-review"]` | 配置层跳过（实际靠 workflow if） |
| `[github_action_config]` | `auto_review` | `true` | PR 打开时自动 review |
| | `auto_describe` | `true` | PR 打开时自动生成描述 |
| | `auto_improve` | `false` | 不自动给修复建议（手动 /improve） |
| `[pr_reviewer]` | `require_estimate_effort_to_review` | `true` | 精力评估 1-5 |
| | `require_tests_review` | `false` | 无测试框架时关闭 |
| | `require_security_review` | `true` | 安全问题分析 |
| | `require_can_be_split_review` | `true` | 大 PR 建议拆分 |
| | `enable_review_labels_effort` | `true` | 打精力标签 |
| | `enable_review_labels_security` | `true` | 打安全标签 |
| | `enable_help_text` | `false` | 去掉底部 Tips |
| | `extra_instructions` | 游戏业务规则 | 核心定制点 |
| `[pr_description]` | `publish_labels` | `true` | 自动打 PR 类型标签 |
| | `keep_original_user_description` | `true` | 保留 PR 模板 checklist |
| | `include_generated_by_header` | `false` | 去掉水印 |
| `[pr_code_suggestions]` | `num_code_suggestions` | `4` | /improve 最多 4 条 |
| | `focus_only_on_problems` | `true` | 只输出 bug，不输出风格 |
| | `suggestions_score_threshold` | `5` | 低于 5 分的建议不显示 |

### PR 评论交互命令

| 命令 | 功能 |
|------|------|
| `/review` | 手动触发 review |
| `/describe` | 重新生成 PR 描述 |
| `/improve` | 给出代码修复建议（含 diff） |
| `/ask 问题` | 针对这个 PR 问 AI |
| `/add_docs` | 自动生成文档注释 |
| `/test` | 自动生成测试代码 |

### 自动标签说明

| 标签 | 来源 | 触发条件 |
|------|------|---------|
| `Bug fix` / `Enhancement` / `Tests` / `Other` | auto_describe | 每个 PR 自动打 |
| `Review effort 1/5` ~ `5/5` | auto_review | 每个 PR 自动打 |
| `possible security issue` | auto_review | 有安全问题时打 |
| `skip-ai-review` | 手动 | 开发者手动打，跳过 AI Review |

---

## 五、已知限制和踩坑记录

### PR-Agent 开源版限制

| 限制 | 说明 | 应对 |
|------|------|------|
| 无法阻断合并 | 不设置 GitHub status check | CI + 人工 Approve 做门禁 |
| `ignore_pr_labels` 对 auto actions 无效 | 配置能读到但不检查 | 在 workflow `if` 条件里拦截 |
| 输出格式不可定制 | section 标题 / emoji / 折叠结构写死 | 只能通过 `extra_instructions` 影响内容 |
| 新模型可能不在内置 token 表 | 报 `not defined in MAX_TOKENS` | 配置 `custom_model_max_tokens` |

### Gemini API 免费额度

| 模型 | RPM | RPD |
|------|-----|-----|
| gemini-2.5-flash | 10 | 20 |
| gemini-2.5-flash-lite（当前） | 15 | 1000 |
| gemini-2.5-pro | 5 | 100 |

一次 auto_describe + auto_review = 2 次 API 调用。1000 RPD 支撑约 500 个 PR/天。

### 常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| PR-Agent 没有评论 | 模型不在 MAX_TOKENS 表 | 加 `custom_model_max_tokens` |
| PR-Agent 没有评论 | Gemini 日限额用完 | 等第二天或切模型 |
| PR-Agent 评论被模板覆盖 | `keep_original_user_description` 未设 | 加到 `[pr_description]` |
| PR-Agent fallback 到 o4-mini 失败 | 无 OpenAI key | 设 `fallback_models = []` |
| skip 标签不生效 | `ignore_pr_labels` 对 auto 无效 | 在 workflow `if` 里检查标签 |
| CI validate 一直 Waiting | Rulesets 要求 check 但 CI 未触发 | 检查分支是否匹配 push trigger |

---

## 六、按仓库定制清单

迁移到具体仓库时，逐项检查：

- [ ] Secret 配置：`GEMINI_API_KEY`（或 `ANTHROPIC_API_KEY`）
- [ ] `ci.yml`：包管理器、Node 版本、lint/build 命令
- [ ] `ci.yml`：是否加 `tsc --noEmit`
- [ ] `ci.yml`：reviewdog 的 `eslint_flags` 路径
- [ ] `.pr_agent.toml`：`extra_instructions` 补充项目特有规则
- [ ] `.pr_agent.toml`：`require_tests_review` 是否开启
- [ ] `.pr_agent.toml`：`[ignore] glob` 加入项目特有生成文件
- [ ] `pull_request_template.md`：按团队流程调整 checklist
- [ ] `CODEOWNERS`：填写实际代码负责人
- [ ] Rulesets：配置 main 保护（require PR + status check + approval）
- [ ] 创建 `skip-ai-review` 标签
- [ ] CLAUDE.md：编写项目专属的 Claude Code 指引

---

## 七、给主管的 FAQ

**Q: 为什么不让 AI 自动阻断？**
> AI 误判率不低，强制阻断会让开发者忽视 AI 评论。CI + 人工 Approve 是硬门禁，AI 是辅助信息。业界主流（GitHub Copilot Review、CodeRabbit）均如此。

**Q: 小改动也跑 AI 浪费吗？**
> Gemini flash-lite 免费 1000 次/天，30 秒出结果，不阻塞任何人。小改动 AI 会标 `effort: 1/5`，Reviewer 秒过。批量翻译类 PR 打 `skip-ai-review` 标签跳过。

**Q: 切 Claude 要改多少？**
> 改 `pr-agent.yml` 里两行环境变量，注释 Gemini 取消注释 Claude。审查规则在 `.pr_agent.toml`，跟模型无关。

**Q: 数据安全？**
> PR-Agent 自托管，代码 diff 只发给你配置的 AI API（Gemini/Claude），不经过任何第三方。
