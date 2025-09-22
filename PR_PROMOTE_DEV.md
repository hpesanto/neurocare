Title: promote: move development -> main

This PR promotes the tested `development` branch into `main`.

Summary:
- `development` currently contains several fixes and feature improvements (menu system, UUID URL fixes, env-based settings, etc.).
- This PR will bring those changes into `main` so `main` reflects the current development-ready code.

Merge plan: merge commit (preserve history). If you prefer squash or rebase, let me know.

Checks to confirm after merge:
- Run migrations and smoke tests in production-like environment
- Verify user authentication and critical flows

If branch protection or required checks prevent an automatic merge, I will report the failure and provide the PR URL for you to review.
