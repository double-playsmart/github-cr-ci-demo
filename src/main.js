import "./style.css";

const checkpoints = [
  {
    title: "Code Review",
    detail: "Use pull requests, PR templates, CODEOWNERS, and review comments."
  },
  {
    title: "Continuous Integration",
    detail: "Run lint and build checks on every push and pull request."
  },
  {
    title: "AI Shared Context",
    detail: "Keep demo goals, scripts, and next steps in docs for multi-AI handoff."
  }
];

const app = document.querySelector("#app");

app.innerHTML = `
  <main class="shell">
    <section class="hero hi">
      <p class="eyebrow">Front-end demo for GitHub workflow</p>
      <h1>Small codebase, visible CR and CI process.</h1>
      <p class="intro">
        This project exists to demonstrate a basic GitHub collaboration pipeline:
        branch, pull request, automated checks, and reviewer guidance.
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
    <section class="flow">
      <h2>Suggested demo flow</h2>
      <ol>
        <li>Create a feature branch.</li>
        <li>Make a tiny UI change.</li>
        <li>Open a pull request.</li>
        <li>Let CI run lint and build.</li>
        <li>Review with checklist and merge.</li>
      </ol>
    </section>
  </main>
`;
