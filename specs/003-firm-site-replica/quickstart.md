# Quickstart: Firm public site (Next.js) — `003-firm-site-replica`

**Branch**: `003-firm-site-replica`  
**Date**: 2026-03-29

This document applies once **`apps/firm-site/`** exists per [plan.md](./plan.md). Until scaffolding lands, treat this as the **target** local-dev checklist.

## Prerequisites

- **Node.js 20 LTS**
- **npm** (root **workspaces** — install once at repo root). **pnpm** works only if you add a `pnpm-workspace.yaml`; this repo defaults to **npm**.

## Bootstrap (when implemented)

```bash
cd /path/to/Law-Office
npm install
cd apps/firm-site
cp .env.example .env.local   # add analytics keys, form secrets, etc.
npm run dev
```

Open `http://localhost:3000`.

## Reference materials

- **HTML snapshots:** `documents/lawyersharma-com/` (source-only reference; **do not** ship as production HTML).
- **Sitemap-derived URLs:** use as a **route checklist** for parity (**SC-002**).

## Performance smoke (local or staging)

```bash
npm run build && npm start
# In another terminal: Lighthouse against http://localhost:3000/ (home, /contact-us, /practice-areas)
```

Document the **exact** network throttle profile used to match **SC-001** in the project `README` or `docs/perf.md`.

## Tests

```bash
npm run test:e2e     # Playwright
npm run lint
```

## Environment variables (representative)

| Variable | Purpose |
|----------|---------|
| `NEXT_PUBLIC_SITE_URL` | Canonical URL for OG tags and sitemap |
| `CONTACT_FORM_TO_EMAIL` | Inbound lead address (if using email) |
| `RESEND_API_KEY` | Or other mail provider (**secret**) |
| `NEXT_PUBLIC_ANALYTICS_ID` | Optional; omit if no analytics |

**Never commit** `.env.local` or real secrets.

## References

- [spec.md](./spec.md) — requirements
- [research.md](./research.md) — stack decisions
- [data-model.md](./data-model.md) — content entities
