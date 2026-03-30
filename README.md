# Law-Office

Monorepo for firm tooling and the public marketing site. **Package manager: npm** (workspaces under `apps/*`).

## Prerequisites

- **Node.js 20 LTS** — for `apps/firm-site` (Next.js)

---

## Firm public website (`apps/firm-site`)

Next.js app: **http://localhost:3000** in development.

### First time

```bash
git clone <your-fork-or-remote> Law-Office
cd Law-Office
npm install
```

Install pulls dependencies for all npm workspaces (including `firm-site`).

### Run the dev server

From the **repository root**:

```bash
npm run firm-site:dev
```

Or from the app folder:

```bash
cd apps/firm-site
npm run dev
```

Open **http://localhost:3000**.

### Environment (optional for local dev)

```bash
cd apps/firm-site
cp .env.example .env.local
# Set NEXT_PUBLIC_SITE_URL when you care about canonical URLs / sitemap (e.g. https://www.example.com)
```

### Other useful commands

| Goal | Command |
|------|---------|
| Production build | `npm run firm-site:build` (from root) or `cd apps/firm-site && npm run build` |
| Run production build locally | `cd apps/firm-site && npm run start` (after `npm run build`) |
| Lint | `npm run firm-site:lint` (from root) |
| E2E tests (Playwright) | `cd apps/firm-site && npm run test:e2e` |

More detail: [apps/firm-site/README.md](apps/firm-site/README.md).

---

## TODO (next feature branch)

These items are tracked in `specs/003-firm-site-replica/tasks.md` (T037–T041).

- **T037 (FR-006)**: Finalize pre-launch operations guidance and ensure the checklist is linked and kept current: `apps/firm-site/docs/launch-checklist.md`
- **T038 (FR-007)**: Add a dedicated **Privacy Notice** page (forms + booking data flows, subprocessors, retention/deletion, disclaimers)
- **T039 (FR-007)**: Implement real contact submission handling (`apps/firm-site/src/app/contact-us/actions.ts`) to firm-approved email/CRM via env secrets (no PII in URLs; avoid logging message bodies)
- **T040 (FR-007)**: Add server-side least-data validation + optional consent capture (checkbox + timestamp/version)
- **T041 (FR-007)**: Add abuse controls (minimum: rate limiting; optional: CAPTCHA) and document behavior in the launch checklist

---

## USCIS PDF fill — local tool (`apps/uscis-fill-local`)

This tool is planned to be **ported to JavaScript** and integrated into the broader product. Until that migration work is scheduled, treat this folder as legacy/experimental.

---

## Repository layout

```text
Law-Office/
├── apps/
│   ├── firm-site/          # Next.js public site (npm workspace)
│   └── uscis-fill-local/   # Legacy POC (planned JS port)
├── documents/              # Reference assets (e.g. crawled HTML)
├── specs/                  # Feature specs and plans
├── package.json            # npm workspaces root
└── README.md               # this file
```

---

## Specs

Feature documentation lives under `specs/` (e.g. `specs/003-firm-site-replica/` for the public site).
