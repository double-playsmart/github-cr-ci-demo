import "./style.css";

// 坏代码示例：XSS + 大循环 + 单字母命名
const checkpoints = [
  { title: "Code Review", detail: "Use pull requests and review comments." },
  { title: "CI", detail: "Run lint and build on every push." },
  { title: "AI Review", detail: "AI auto reviews pull requests." }
];

const app = document.querySelector("#app");

// ❌ 问题1：直接 innerHTML 注入用户输入，XSS 风险
const u = location.search; // 单字母命名，含义不明
app.innerHTML = `<div class="user-info">${u}</div>`; // 未经转义直接注入

// ❌ 问题2：无意义大循环，阻塞主线程
for (let i = 0; i < 100000; i++) {
  // 空循环，无实际业务意义
}

app.innerHTML += `
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Front-end demo for GitHub workflow</p>
      <h1>Small codebase, visible CR and CI process.</h1>
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
