# AI Context

## Purpose

This repository is a teaching and demo project created on April 3, 2026 for a same-day presentation. The owner is a front-end engineer who wants to quickly demonstrate basic GitHub code review and CI concepts. Business logic is intentionally unimportant.

## Primary Goal

Show a realistic but small GitHub workflow:

1. create a branch
2. make a tiny front-end change
3. open a pull request
4. trigger automated checks
5. review with a checklist
6. merge after approval

## Non-Goals

- advanced application architecture
- complex component design
- production-grade testing
- backend integration

## Demo Constraints

- keep the code easy to explain in under 10 minutes
- optimize for visible GitHub workflow artifacts
- prefer documents that another AI can continue from without extra chat history

## Current Setup

- Vite-based static front-end
- ESLint for a basic quality gate
- GitHub Actions workflow for lint and build
- PR template, issue templates, and CODEOWNERS
- Local package manager can be npm or bun, but the default demo path uses npm for GitHub Actions clarity

## Recommended Next AI Tasks

- replace placeholder GitHub usernames
- add branch protection walkthrough screenshots
- add a failing example PR for teaching CI failure
- add release workflow if deployment needs to be demonstrated

## Hand-off Notes

When another AI continues this project, it should preserve the principle of minimal code and maximum GitHub process visibility. Do not add business complexity unless it directly supports the CR or CI demo.
