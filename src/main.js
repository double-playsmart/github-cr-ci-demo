import "./style.css";

const checkpoints = [
  { title: "Code Review", detail: "通过 PR 模板、CODEOWNERS 和 AI Review 规范代码审查流程。" },
  { title: "Continuous Integration", detail: "每次 push 和 PR 自动运行 lint + build，失败时阻断合并。" },
  { title: "AI Review", detail: "PR-Agent 接入 Gemini/Claude，自动输出中文审查意见，支持 /ask 交互。" }
];

const app = document.querySelector("#app");

app.innerHTML = `
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">GitHub CR / CI 演示</p>
      <h1>小仓库，看得见的 Code Review 和 CI 流程。</h1>
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
