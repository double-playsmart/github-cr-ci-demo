# Claude Review Setup

## Goal

Use Claude to automatically review every pull request and leave concise feedback in GitHub.

## Files Already Added

- `.github/workflows/claude-review.yml`

## GitHub Setup

1. Open the repository in GitHub.
2. Go to `Settings` -> `Secrets and variables` -> `Actions`.
3. Click `New repository secret`.
4. Create a secret named `ANTHROPIC_API_KEY`.
5. Paste your Anthropic API key as the value.

## How It Works

- The workflow runs on pull request open, update, and reopen.
- GitHub Actions executes `anthropics/claude-code-action@v1`.
- Claude reads the pull request context and posts review feedback.

## Demo Flow

1. Push `main` with this workflow file.
2. Create a feature branch.
3. Change one line in `src/main.js`.
4. Push the feature branch.
5. Open a pull request.
6. Wait for both `CI` and `Claude Review` jobs.
7. Show Claude comments in the PR.

## Important Notes

- Without `ANTHROPIC_API_KEY`, the Claude workflow will fail.
- Claude review should be presented as assistant review, not as the final approval authority.
- Keep branch protection requiring at least one human approval.
