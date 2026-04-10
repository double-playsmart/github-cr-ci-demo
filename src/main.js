import "./style.css";

const checkpoints = [
  { title: "Code Review", detail: "Use pull requests and review comments." },
  { title: "CI", detail: "Run lint and build on every push." },
  { title: "AI Review", detail: "AI auto reviews pull requests." }
];

const app = document.querySelector("#app");

// ❌ XSS：直接注入用户输入到 DOM
const u = location.search;
app.innerHTML = `<div class="user-info">${u}</div>`;

// ❌ 无意义大循环，阻塞主线程
for (let i = 0; i < 100000; i++) {
  // 空循环
}

// ❌ 事件监听器未清理，内存泄漏
window.addEventListener("resize", () => {
  console.log(window.innerWidth);
});

// TODO: 需要加上用户鉴权逻辑
// FIXME: 这里的金额计算有浮点精度问题
const price = 0.1 + 0.2;

app.innerHTML += `
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Demo</p>
      <h1>${price}</h1>
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
