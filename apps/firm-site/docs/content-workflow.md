# Content update workflow (FR-004, SC-004)

## Process

1. **Branch** from `main` for the change.
2. Edit **TSX** pages under `src/app/` or `content/navigation.json` (navigation model).
3. Open a **pull request**; request review from a second maintainer when available.
4. **Preview** on the hosting provider’s preview URL (e.g. Vercel) when configured.
5. **Merge** → production deploy.

## Routine edit dry-run (SC-004)

After maintainer training, complete once:

- [ ] Change one paragraph on a non-critical page (e.g. **Payment** page copy).
- [ ] Swap `public/images/` asset with an optimized replacement (same filename or update `next/image` props).
- [ ] Verify **build** (`npm run build`) and **smoke** (`npm run test:e2e`) locally or in CI.
- [ ] Confirm deploy completes within **one business day** of the trained maintainer starting (excluding blockers outside their control).

**Sign-off:** **\*\*\*\***\_**\*\*\*\*** **Date:** **\*\*\*\***\_**\*\*\*\***
