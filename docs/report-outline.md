# Report Outline

## 1. Why This Demo Exists

- I am a front-end engineer.
- The goal is not business logic.
- The goal is to show a basic GitHub collaboration loop.

## 2. What Is Code Review In GitHub

- work on branches instead of direct commits to `main`
- open pull requests for every change
- let reviewers focus on risk, scope, and clarity
- use templates and CODEOWNERS to standardize review

## 3. What Is CI In GitHub

- GitHub Actions runs checks automatically
- every push or PR can trigger validation
- this demo uses two simple checks: lint and build
- CI prevents obviously broken code from being merged

## 4. Demo Flow

1. create a branch
2. change one line in the front-end
3. push the branch
4. open a PR
5. show the PR template
6. wait for CI to pass
7. simulate review and merge

## 5. Why This Matters

- smaller review cost
- clearer ownership
- lower merge risk
- visible engineering process

## 6. How To Evolve Later

- add test coverage
- add preview deployment
- add stricter protection rules
- add automated release process
