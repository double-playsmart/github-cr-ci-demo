# Demo Script

## 5-Minute Version

1. Open the repository root and explain that the front-end is intentionally tiny.
2. Show `.github/pull_request_template.md` and `.github/CODEOWNERS`.
3. Show `.github/workflows/ci.yml` and explain lint plus build on PR.
4. Create a branch and modify a short sentence in `src/main.js`.
5. Push to GitHub and open a PR.
6. Walk through the template and the review focus section.
7. Wait for checks to pass, then explain merge rules.

## 10-Minute Version

1. Start from `README.md` to explain the repository goal.
2. Open `docs/ai-context.md` to show AI-shareable project background.
3. Open `docs/demo-script.md` to show the planned presentation path.
4. Show the issue templates as examples of structured collaboration.
5. Walk into the workflow file and explain event triggers and steps.
6. Demonstrate a small code change and explain why CI should stay fast.
7. Open a PR and describe reviewer expectations.
8. Mention branch protection settings to be configured in GitHub UI.

## Optional Failure Demo

- Introduce an obvious lint error in `src/main.js`.
- Push to the feature branch.
- Show the failed GitHub Action.
- Fix the error and push again to show recovery.
