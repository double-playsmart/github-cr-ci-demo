import "./style.css";

const checkpoints = [
  {
    title: "Code Review",
    detail: "通过 Pull Request 流程做代码审查，配合 PR 模板、CODEOWNERS 和 Review 评论。"
  },
  {
    title: "Continuous Integration",
    detail: "每次 push 和 PR 自动触发 lint + build 检查，失败时阻断合并。"
  },
  {
    title: "AI Review",
    detail: "Gemini 自动读取 PR diff，按五个维度打分，评分不足时自动阻断合并。"
  }
];

const app = document.querySelector("#app");

app.innerHTML = `
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">GitHub 工作流演示 · 游戏组前端</p>
      <h1>最小代码，完整的 CR 和 CI 流程。</h1>
      <p class="intro">
        这个项目演示一套基础的 GitHub 协作链路：
        切分支 → 提 PR → 自动检查 → AI Review → 人工 Approve → 合并。
      </p>
    </section>
    <section class="grid">
      ${checkpoints
        .map(
          (item) => `
            <article class="card">
              <h2>${item.title}</h2>
              <p>${item.detail}</p>
            </article>
          `
        )
        .join("")}
    </section>
  </main>
`;
