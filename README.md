# GitHub CR / CI Demo

This repository is a minimal front-end project built for a fast demo of GitHub collaboration workflows. The app is intentionally simple. The focus is:

- code review through pull requests
- continuous integration through GitHub Actions
- optional AI review through Claude on pull requests
- AI-shareable project context through structured docs

## Quick Start

```bash
npm install
npm run check
```

Optional:

```bash
bun install
bun run lint
bun run build
```

## What To Demo

1. Create a repository on GitHub and push this folder.
2. Replace the placeholder in `.github/CODEOWNERS`.
3. Create a feature branch such as `feature/update-hero-copy`.
4. Change a small UI text in `src/main.js`.
5. Push and open a pull request.
6. Show the PR template, review checklist, and CI checks.
7. Merge after review approval.

## Repository Structure

- `src/`: minimal front-end files
- `.github/`: GitHub review and CI configuration
- `docs/`: reusable context for human and AI collaborators

## Suggested GitHub Settings

- Protect `main`
- Require at least one approval
- Require status checks before merge
- Require conversation resolution before merge
- Require review from code owners
- Disable direct push to protected branch

## Core Commands

```bash
npm run dev
npm run lint
npm run build
npm run check
```

## Optional Claude Review

If you want Claude to review every pull request automatically:

1. Add the repository secret `ANTHROPIC_API_KEY`
2. Keep `.github/workflows/claude-review.yml` enabled
3. Open or update a pull request

Claude review is an extra review layer. It does not replace human approval or CI.
