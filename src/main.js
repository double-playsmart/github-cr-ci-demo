import "./style.css";

// 🔴 硬编码 API Key（敏感信息泄露）
const API_KEY = "sk-ant-api03-xK9mN2pL8qR5vT1wY4zA7bC0dE6fG3hI-FAKE";
const API_SECRET = "ghp_FakeGitHubToken1234567890abcdefXYZ";

// 🔴 敏感信息直接拼入请求头
async function fetchUserData(userId) {
  const res = await fetch(`/api/users/${userId}`, {
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "X-Secret": API_SECRET,
    },
  });
  return res.json();
}

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

// 🔴 XSS：直接将 URL 参数注入 innerHTML
const params = new URLSearchParams(window.location.search);
const username = params.get("user") || "访客";
const userId = params.get("id");
document.querySelector("#app").innerHTML = `<p>欢迎，${username}</p>`;
if (userId) fetchUserData(userId);

// 🔴 XSS：eval 执行用户输入
function runUserCode(input) {
  eval(input);
}

const codeParam = params.get("code");
if (codeParam) runUserCode(codeParam);

// 🔴 内存泄漏：事件监听器从未清理
function setupSearch() {
  const handler = () => console.log("searching...");
  for (var i = 0; i < 100; i++) {
    document.addEventListener("keydown", handler);
  }
}
setupSearch();

// 🟡 使用 var + 无意义命名
var x = 0;
var y = 0;
for (var i = 0; i < 50000; i++) {
  x = x + i;
  y = y + x;
}

const app = document.querySelector("#app");

app.innerHTML = `
  <main class="shell">
    <section class="hero">
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
  </main>
`;
