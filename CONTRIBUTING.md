# Contributing Guide

## Branch Naming

- `feature/<short-description>`
- `fix/<short-description>`
- `docs/<short-description>`

## Pull Request Rules

- keep PRs small enough for a reviewer to read quickly
- explain the reason, not only the code diff
- list the commands you ran locally
- mark what the reviewer should focus on

## Local Validation

```bash
npm run lint
npm run build
```

## Review Standard

- Is the change easy to understand?
- Is the risk visible in the PR description?
- Did CI pass?
- Is the merge target correct?
