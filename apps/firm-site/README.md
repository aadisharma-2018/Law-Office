# Firm public site (`apps/firm-site`)

**Install and run:** see the [root README](../../README.md) (`npm install` at repo root, then `npm run firm-site:dev`).

Next.js (**App Router**) + **TypeScript** + **Tailwind CSS**. **v1** is **TSX-first**: routes live under `src/app/` as `page.tsx` files. **MDX** in `content/` is optional for a later increment (**FR-004**).

## Scripts

| Command                       | Description                                                      |
| ----------------------------- | ---------------------------------------------------------------- |
| `npm run dev`                 | Dev server (Turbopack)                                           |
| `npm run build` / `npm start` | Production build & server                                        |
| `npm run lint`                | ESLint (Next core-web-vitals)                                    |
| `npm run format`              | Prettier                                                         |
| `npm run test:e2e`            | Playwright (smoke, a11y, internal links)                         |
| `npm run test:e2e:a11y`       | axe on key templates                                             |
| `npm run check-links`         | SC-002 internal URL check                                        |
| `npm run lhci`                | Lighthouse CI (after `build` + `start`; see `lighthouserc.json`) |

## Environment

Copy `.env.example` to `.env.local` and set `NEXT_PUBLIC_SITE_URL` for staging/production.

## Adding a route

1. Create `src/app/<segment>/page.tsx` (and `layout.tsx` if needed).
2. Add internal links to `content/navigation.json` when the page should appear in header/footer.
3. Extend `src/app/sitemap.ts` if you add paths outside `getAllInternalPaths()` (it derives from nav + service slugs).

## API / server actions

- **Health:** `GET /api/health` — JSON `{ "status": "ok" }` for monitors.
- **Contact form:** stub in `src/app/contact-us/` — enable after mail/CRM secrets and **FR-007** privacy review.

## Docs

- Performance: `docs/perf.md`
- Usability study template: `docs/usability-study.md`
- Maintainer workflow: `docs/content-workflow.md`

## Reference

Static HTML snapshots: `documents/lawyersharma-com/` (not served as production HTML).
