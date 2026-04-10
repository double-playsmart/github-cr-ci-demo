# AI Code Review 方案说明

> PR-Agent（自动审查）+ @claude（手动深度分析）的组合方案。
> 适用于迁入 GitHub 后的前端项目。

---

## 1. 这是什么？

### 1.1 简介

采用两套工具组合：

| 工具 | 角色 | 触发方式 | 计费 |
|------|------|---------|------|
| **PR-Agent** | 自动审查（describe + review + 标签） | PR 创建时自动触发 | API token 按量付费 |
| **@claude** | 手动深度分析 | PR 评论区输入 `@claude 问题` | 使用 Claude 订阅额度（不额外付费） |

PR-Agent 负责每个 PR 的自动覆盖（低成本跑量），@claude 负责复杂问题的深度分析（免费，可读整个仓库上下文）。

### 1.2 方案选型

当前采用 **PR-Agent + @claude 组合方案**：

| 方案 | 角色 | 成本 | 结论 |
|------|------|------|------|
| **PR-Agent** | 自动审查（标签/评分/TODO/精力评估） | ~$0.006/次（API） | ✅ 主力 |
| **@claude GitHub App** | 手动深度分析（读整个仓库） | 订阅额度（不额外付费） | ✅ 补充 |

其他方案对比：

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| claude-code-action（自动化） | 可阻断合并 | 功能需自己写 prompt，API 成本高 15 倍 | 不采用 |
| Claude Code Review（托管） | 深度分析 | $15-25/次 | ❌ 太贵 |
| CodeRabbit | 开箱即用 | 2025 年 RCE 漏洞 | ❌ |
| GitHub Copilot Review | 微软官方 | 锁定 GitHub + OpenAI | 备选 |


### 1.3 数据安全

自托管模式，代码 diff 只发给配置的 AI API（Claude/Gemini/GPT），不经过 PR-Agent 或任何第三方服务器。



---

## 2. 接入后 PR 流程会怎样？

### 2.1 默认行为

提 PR 到 main 后约 30 秒内自动触发，无需人工操作：

```
提 PR → PR-Agent 自动运行
  ├── 生成 PR 描述（写入描述框，保留原有模板）
  ├── 发 Review 评论（精力评估 + 安全分析 + 审查重点）
  └── 打标签（Bug fix / Enhancement / Review effort 2/5 等）
```

### 2.2 触发条件


| 事件                      | 是否触发  | 可配置  |
| ----------------------- | ----- | ---- |
| PR 创建（opened）           | ✅ 触发  | 可关闭  |
| PR 重新打开（reopened）       | ✅ 触发  | 可关闭  |
| 草稿转正式（ready_for_review） | ✅ 触发  | 可关闭  |
| PR 有新 push（synchronize） | ❌ 不触发 | 可开启  |
| 评论区输入命令                 | ✅ 触发  | 始终可用 |


### 2.3 可用命令

在 PR 评论区输入，约 30 秒出结果：


| 命令                  | 功能                    |
| ------------------- | --------------------- |
| `/review`           | 手动触发 review           |
| `/improve`          | 代码修复建议，直接贴在 diff 对应行上 |
| `/ask 问题`           | 针对这个 PR 提问            |
| `/describe`         | 重新生成 PR 描述            |
| `/add_docs`         | 自动生成函数文档注释            |
| `/update_changelog` | 自动更新 CHANGELOG        |

### 2.4 @claude 手动深度分析

在 PR 评论区输入 `@claude` + 问题，Claude 会读取整个仓库上下文进行分析：

```
@claude 这个改动会影响其他模块的状态管理吗？
@claude 帮我 review 这段 WebSocket 处理逻辑的竞态问题
@claude 这个组件的性能优化方向是什么
```

与 PR-Agent `/ask` 的区别：

| | PR-Agent `/ask` | @claude |
|---|---|---|
| 上下文 | 只看 PR diff | 可读整个仓库 |
| 模型 | 当前配置的模型（Haiku） | Claude Sonnet（订阅档位） |
| 计费 | API token（额外付费） | 订阅额度（不额外付费） |
| 适合 | 简单问题 | 复杂架构 / 跨模块分析 |

@claude 通过已安装的 Claude GitHub App 触发，无需额外配置 workflow。

---

## 3. AI 会阻断我的合并吗？

**不会。**

PR-Agent 只发评论和打标签，不设置 GitHub status check，无法阻断合并。

阻断合并的是：

- **CI（lint / type check / build）** — 失败时 Rulesets 阻断
- **人工 Approve** — 至少 1 人批准

AI Review 的定位是**辅助信息**，不是决策者。原因：

- AI 误判率不低，强制阻断会导致开发者被误判卡住，最终忽视 AI 评论
- 业界主流工具（GitHub Copilot Review、CodeRabbit）均不阻断
- 正确流程：AI 提供信息 → Reviewer 看 AI 评论做判断 → 人 Approve

---

## 4. 怎么跳过 AI Review？

### 4.1 单个 PR 跳过

创建 PR 时打 `skip-ai-review` 标签，PR-Agent 不会启动。适合批量翻译、配置变更等不需要审查的 PR。

命令行：

```bash
gh pr create --label "skip-ai-review" --title "..." --body "..."
```

### 4.2 关闭自动触发（仅保留手动命令）

修改 `pr-agent.yml`，删掉 `pull_request` 触发，只保留 `issue_comment`：

```yaml
on:
  issue_comment:
```

关闭后 PR-Agent 不会自动启动，只有在评论区输入 `/review` 等命令才会触发。

---

## 5. 怎么接入我的仓库？

### Step 1：添加 Secret

仓库 → Settings → Secrets and variables → Actions → New repository secret


| Secret              | 来源                                                      |
| ------------------- | ------------------------------------------------------- |
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/) |


Gemini 免费但额度低（20 次/天），建议直接用 Claude。

### Step 2：复制两个文件

1. `.github/workflows/pr-agent.yml` — 触发入口
2. `.pr_agent.toml` — 审查规则配置

从 demo 仓库直接复制，根据项目调整 `extra_instructions`。

### Step 3：创建 skip 标签

```bash
gh label create "skip-ai-review" --color "ededed" --description "跳过 AI Review"
```

---

## 6. 怎么定制审查规则？

### 6.1 extra_instructions

`.pr_agent.toml` 中的 `extra_instructions` 是核心定制点，用自然语言描述审查规则：

```toml
[pr_reviewer]
extra_instructions = """
你是一位资深前端工程师。审查时重点关注：

【安全性】
- 禁止 innerHTML 直接注入用户输入
- 敏感信息不得出现在代码中

【性能】
- 避免无意义大循环
- 事件监听器必须清理

【业务专项】
- 赔率计算检查浮点精度
- WebSocket 消息处理考虑竞态条件
"""
```

修改后 push 即生效，无需其他操作。可针对仓库特性自定义审查规则。

### 6.2 best_practices.md

在仓库根目录创建 `best_practices.md`，写入团队编码规范。PR-Agent 会自动读取并在 review 时参考，违反规范会额外标注。

### 6.3 忽略文件

```toml
[ignore]
glob = [
  "*.lock", "dist/**", "node_modules/**",
  "src/locales/**",    # 翻译文件
]
```

---

## 7. 用哪个模型？多少钱？

### 7.1 模型对比

以中等 PR（~15K token）单次 review 估价：


| 模型                | 单次 review | 100 次/天 | 数据安全    | 适合      |
| ----------------- | --------- | ------- | ------- | ------- |
| Claude Haiku      | ~$0.006   | ~$0.6   | 最好（不留存） | demo/测试 |
| Claude Sonnet ⭐   | ~$0.06    | ~$6     | 最好（不留存） | 正式项目推荐  |
| GPT-4o mini       | ~$0.004   | ~$0.4   | 留存 30 天 | 省钱      |
| GPT-4o            | ~$0.05    | ~$5     | 留存 30 天 | 生态最广    |
| Gemini Flash Lite | ~$0.002   | ~$0.2   | 留存 30 天 | 最便宜     |
| Gemini Flash ⭐    | ~$0.008   | ~$0.8   | 留存 30 天 | 性价比     |


### 7.2 切换方法

编辑 `.github/workflows/pr-agent.yml`，注释/取消注释对应模型行即可。审查规则在 `.pr_agent.toml` 中，跟模型无关，切换不需要改规则。

### 7.3 Gemini 免费层

Gemini 有免费额度但只有 20 RPD/天（一天最多 10 个 PR），适合 demo 验证，正式使用建议付费。

---

## 8. 其他常见问题

**Q: PR-Agent 评论没出现？**

> 检查 Actions 页面的 PR Agent workflow 日志。常见原因：API 额度用完、模型不在内置 token 表（需配 `custom_model_max_tokens`）。

**Q: 评论都是英文？**

> 检查 `.pr_agent.toml` 是否配置了 `response_language = "zh-CN"`。

**Q: /improve 没有行内评论？**

> 需要配置 `commitable_code_suggestions = true`。如果 AI 判断无可改进内容，会返回空结果。

**Q: 能自动合并吗？**

> PR-Agent 不支持自动合并。GitHub 的 auto-merge 功能需要单独开启，与 PR-Agent 无关。

**Q: 换模型要改审查规则吗？**

> 不用。模型在 `pr-agent.yml` 里配，规则在 `.pr_agent.toml` 里配，互相独立。

**Q: 多个仓库能共享配置吗？**

> 可以把 `.pr_agent.toml` 放在 GitHub Organization 的 `.github` 仓库里作为全局配置，也可以用 Wiki 配置（不需要提交到代码仓库）。

**Q: @claude 和 PR-Agent /ask 有什么区别？**

> @claude 使用订阅额度（不额外花钱），可以读整个仓库上下文，模型更强（Sonnet）。/ask 用 API token（额外付费），只看 PR diff。简单问题用 /ask，复杂架构问题用 @claude。

**Q: @claude 需要额外配置吗？**

> 不需要。安装 Claude GitHub App 后直接可用，在 PR 评论区输入 `@claude 问题` 即可。

