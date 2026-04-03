# GitHub Setup Checklist

## Repository Setup

1. Create an empty GitHub repository.
2. Add this local project as the remote.
3. Rename local branch to `main`.
4. Push the first commit.

Example commands:

```bash
git branch -M main
git remote add origin <your-github-repo-url>
git add .
git commit -m "chore: bootstrap github cr ci demo"
git push -u origin main
```

## Branch Protection

In GitHub:

1. Open `Settings` -> `Branches`.
2. Add a protection rule for `main`.
3. Enable required pull request reviews.
4. Enable required status checks.
5. Select the `CI / validate` check after the workflow runs once.
6. Optionally disable force pushes and branch deletion.

## Review Demo

1. Create `feature/demo-pr`.
2. Edit one sentence in `src/main.js`.
3. Push and open a PR.
4. Fill the PR template.
5. Request a reviewer.
6. Show the passing CI result.

## CI Failure Demo

1. Add an unused variable in `src/main.js`.
2. Push to the feature branch.
3. Show the failed lint check in GitHub.
4. Remove the error and push again.
