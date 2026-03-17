---
name: "Create Pull Request"
description: "Create a GitHub pull request with a structured title/body, assign the current user, and leave review and merge decisions manual."
argument-hint: "Target branch, base branch, and PR summary"
agent: "agent"
---
# Create Pull Request Prompt

Create a pull request for the current branch using GitHub CLI when available.

Workflow:

1. Confirm the current branch, base branch, and working tree state.
2. Create the PR with a concise, structured title and body.
3. Add the current user as assignee with `gh pr edit <pr> --add-assignee "@me"`.
4. Leave reviewers, labels, projects, and milestone available for manual follow-up unless explicitly requested.
5. Do not enable auto-merge by default.

Output requirements:

- Report the PR URL.
- State whether the assignee was added successfully.
- State that review, labels, projects, milestone, and merge remain manual unless explicitly requested.
- Mention any missing GitHub auth or permission scopes.
