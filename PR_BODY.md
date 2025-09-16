Title: chore: sync development branch with pending changes

Summary:
This PR brings the current local development work into the `development` branch on remote. It includes configuration hardening and environment-driven settings:

- Read SECRET_KEY, DEBUG and DB settings from environment variables.
- Replace print warnings in DB selection with logging.
- Add Django password validators.
- Add `.env.example` and update README with environment variable instructions.

Security notes / required follow-ups:
- Confirm `.env` does not contain real secrets. If it does, remove it from the repo (`git rm --cached .env`) and rotate credentials.
- Add `.env` to `.gitignore` to prevent accidental commits of secrets.

Suggested gh command to create the PR (run after `gh auth login`):

```
gh pr create --base main --head development --title "chore: sync development branch with pending changes" --body-file PR_BODY.md
```

Alternatively, open the PR in the browser: https://github.com/hpesanto/neurocare/pull/new/development
