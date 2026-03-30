# Tasks: Rebuild firm public website from reference materials (performance-ready)

**Input**: Design documents from `specs/003-firm-site-replica/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [data-model.md](./data-model.md), [research.md](./research.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: [research.md](./research.md) calls for **Playwright** and **Lighthouse**-style checks; included in **Polish** and **US2** where they validate **SC-001**/**SC-002**. Not full TDD unless extended later.

**Organization**: Phases follow [spec.md](./spec.md) user stories **US1** (P1), **US2** (P1), **US3** (P2).

**Root paths**: Relative to repository root `Law-Office/`. New app: **`apps/firm-site/`** per [plan.md](./plan.md). Reference HTML: **`documents/lawyersharma-com/`** (read-only).

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Parallelizable (different files, no ordering dependency within the same phase)
- **[USn]**: Maps to User Story _n_ in [spec.md](./spec.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize **Next.js** + **TypeScript** + **Tailwind** + tooling per [plan.md](./plan.md).

- [x] T001 Create `apps/firm-site/` scaffold: `package.json`, `tsconfig.json`, `next.config.ts`, `postcss.config.mjs`, `tailwind.config.ts`, `.gitignore`, and `README.md` with scripts (`dev`, `build`, `start`, `lint`)
- [x] T002 Add `apps/firm-site/src/app/layout.tsx` (minimal shell) and `apps/firm-site/src/app/page.tsx` (placeholder) plus `apps/firm-site/src/app/globals.css` with Tailwind directives
- [x] T003 [P] Configure ESLint and Prettier for `apps/firm-site/` (flat config or `eslint.config.mjs`; `prettier` if not repo-wide)
- [x] T004 [P] Add `apps/firm-site/.env.example` with `NEXT_PUBLIC_SITE_URL` and placeholders for optional analytics/form secrets per [quickstart.md](./quickstart.md)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared **layout**, **navigation model**, and **content folders** required by all pages. **No story-specific page copy** until this phase completes.

- [x] T005 Create `apps/firm-site/content/navigation.json` matching the **navigation model** in [data-model.md](./data-model.md) (header/footer entries and `href`s aligned to planned routes)
- [x] T006 Implement `apps/firm-site/src/components/SiteHeader.tsx` and `apps/firm-site/src/components/SiteFooter.tsx` consuming `content/navigation.json`
- [x] T007 Implement root layout in `apps/firm-site/src/app/layout.tsx`: wrap children with **SiteHeader**/**SiteFooter**, set default `metadata` baseline, and wire **fonts** via `next/font` per [research.md](./research.md)
- [x] T008 Add `apps/firm-site/src/app/not-found.tsx` and `apps/firm-site/src/app/loading.tsx` (or segment-level as needed)
- [x] T009 Create `apps/firm-site/content/pages/` (or `content/mdx/`) and `apps/firm-site/public/images/` with a **README** describing how MDX/frontmatter maps to [data-model.md](./data-model.md) **Published page** fields
- [x] T010 Add `apps/firm-site/src/lib/site.ts` for **canonical URL** / metadata helpers using `NEXT_PUBLIC_SITE_URL`

**Checkpoint**: App runs with `pnpm dev` (or `npm run dev`); chrome shows header/footer on placeholder home.

---

## Phase 3: User Story 1 — Visitors see an equivalent public site (Priority: P1)

**Goal**: **Equivalent** IA and primary journeys vs reference (**FR-001**); routes mirror **`documents/lawyersharma-com/`** sitemap-derived paths from prior crawl.

**Independent Test**: Manual walkthrough of every route in the navigation map; content intent matches reference checklist (**spec** US1 independent test).

### Implementation

- [x] T011 [US1] Implement **home** at `apps/firm-site/src/app/page.tsx` with sections (hero, practice highlights, CTAs) derived from `documents/lawyersharma-com/index.html` content intent (not raw HTML paste)
- [x] T012 [P] [US1] Implement `apps/firm-site/src/app/about-us/page.tsx` with metadata and body content from reference
- [x] T013 [P] [US1] Implement `apps/firm-site/src/app/contact-us/page.tsx` and `apps/firm-site/src/app/copy-of-contact-us/page.tsx` (or consolidate to one canonical contact route with redirect—document choice in `README`)
- [x] T014 [P] [US1] Implement `apps/firm-site/src/app/practice-areas/page.tsx`
- [x] T015 [P] [US1] Implement `apps/firm-site/src/app/book-online/page.tsx` and `apps/firm-site/src/app/payment/page.tsx`
- [x] T016 [P] [US1] Implement `apps/firm-site/src/app/terms/page.tsx` and `apps/firm-site/src/app/disclaimer/page.tsx`
- [x] T017 [US1] Implement **services list** data model (`apps/firm-site/src/data/services.ts`) used to render service summaries; each service routes to `/book-online` until booking is implemented
- [x] T018 [US1] Import firm-owned **images** into `apps/firm-site/public/images/` (optimized filenames); use **`next/image`** with **alt** text for above-the-fold sections on home and key pages (**FR-008**)
- [x] T019 [US1] Add `apps/firm-site/src/app/sitemap.ts` and `apps/firm-site/src/app/robots.ts` for SEO per [research.md](./research.md) §7

**Checkpoint**: **US1** complete—all primary routes reachable, **SC-002** satisfied for internal links in scope (verify in Polish with automation).

---

## Phase 4: User Story 2 — Site feels fast and works on phones (Priority: P1)

**Goal**: Meet **SC-001** on key pages; responsive layout (**FR-003**); image/font performance per [research.md](./research.md).

**Independent Test**: Lighthouse (lab) on home, `/contact-us`, `/practice-areas` using the throttling profile documented in `apps/firm-site/README.md` or `docs/perf.md`.

### Implementation

- [x] T020 [US2] Audit and fix **responsive** layout issues in `apps/firm-site/src/components/` and page templates (breakpoints, no horizontal scroll on main columns) per **FR-003**
- [x] T021 [US2] Ensure **LCP** targets: prioritize **`next/image`** `priority` on hero; explicit **width/height** for static images in `apps/firm-site/src/app/**` and shared components
- [x] T022 [US2] Add `docs/perf.md` or `apps/firm-site/docs/perf.md` documenting the **mobile network profile** and commands used to validate **SC-001**
- [x] T023 [US2] Add **Lighthouse CI** or `lhci` script in `apps/firm-site/package.json` and minimal **budget** config (thresholds aligned with **SC-001**—document assumptions)

**Checkpoint**: **US2** metrics reproducible from documented commands.

---

## Phase 5: User Story 3 — Firm can extend the site later (Priority: P2)

**Goal**: Clear **extension points** for new routes/APIs without re-platforming (**spec** US3, **plan** complexity note).

**Independent Test**: `apps/firm-site/README.md` describes how to add a route and optional **Route Handler**; tabletop “add `/resources/staff` page” succeeds without structural rewrites.

### Implementation

- [x] T024 [US3] Document extension conventions in `apps/firm-site/README.md`: folder structure (`src/app/`), adding MDX, adding **API route** or **Server Action** stubs under `src/app/api/` for future use
- [x] T025 [US3] Add `apps/firm-site/src/app/api/health/route.ts` returning **200** JSON (smoke target for hosting monitors; no sensitive data)
- [x] T026 [US3] Stub optional **contact form** as **Server Action** or `POST` handler placeholder in `apps/firm-site/src/app/contact-us/` (disabled or noop until secrets exist) per [contracts/README.md](./contracts/README.md)—**FR-007** copy reviewed before enabling

**Checkpoint**: **US3** documentation + health route merged; form wiring can follow a future task once SMTP/CRM chosen.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: E2E smoke, **FR-009** notices, privacy/subprocessor alignment, **quickstart** validation.

- [x] T027 [P] Configure **Playwright** in `apps/firm-site/` (`playwright.config.ts`, `tests/e2e/smoke.spec.ts`) visiting home + contact + booking; assert **200** and **no** console errors on load (**smoke** subset; **SC-002** full internal link coverage is **T036**)
- [x] T028 [P] Add `apps/firm-site/THIRD_PARTY_NOTICES.md` (or generate via script) listing **npm** OSS licenses for **FR-009**
- [x] T029 Review **privacy** / **terms** pages for statements about **analytics**, **forms**, and **subprocessors** consistent with [plan.md](./plan.md) table; adjust copy only with firm approval
- [x] T030 Run through [quickstart.md](./quickstart.md) on a clean clone; fix gaps in `apps/firm-site/README.md`
- [x] T031 Add root **`package.json`** workspace entry or document how to run `apps/firm-site` from monorepo root (optional **pnpm workspace**)
- [ ] T037 Add pre-launch **operations guidance** artifact for **FR-006**: hosting + domain cutover, HTTPS, backups, analytics/privacy disclosures, and a “launch checklist” (e.g. `apps/firm-site/docs/launch-checklist.md`) linked from the root `README.md`

### FR-007 (forms/scheduling) completion tasks

> These tasks are required **before enabling** contact submissions or embedding a scheduler/payment provider in production.

- [ ] T038 Add a dedicated **Privacy Notice** page describing form + booking data flows (what is collected, purpose, recipients/subprocessors, retention/deletion contact, and “no attorney-client relationship” notice where applicable)
- [ ] T039 Implement **real** contact submission handling in `apps/firm-site/src/app/contact-us/actions.ts` (deliver to firm-approved email/CRM using env secrets; no PII in URLs; avoid logging message bodies)
- [ ] T040 Add **least-data** server-side validation + optional **consent capture** (checkbox + timestamp/version recorded) consistent with the Privacy Notice
- [ ] T041 Add abuse controls for submissions (minimum: rate limiting; optional: CAPTCHA) and document behavior in `apps/firm-site/docs/launch-checklist.md`

### Post–analysis remediation (SC-003, SC-004, TSX alignment, a11y, SC-002)

| Ref | Issue                             | Task                        |
| --- | --------------------------------- | --------------------------- |
| G1  | **SC-003** usability study        | T032                        |
| G2  | **SC-004** maintainer workflow    | T033                        |
| I1  | **Plan vs tasks** (TSX v1)        | T034 + **`plan.md`** update |
| G3  | **Accessibility** automation      | T035                        |
| G5  | **SC-002** internal link coverage | T036                        |

- [x] T032 [P] Add `apps/firm-site/docs/usability-study.md` with a **moderated test script** for **SC-003** (tasks, ≥5 participants, 90% threshold), **record results** or **approved deferral** with firm sign-off and target date
- [x] T033 Add `apps/firm-site/docs/content-workflow.md` describing **FR-004** update process (Git PR, review, deploy) and a **dry-run checklist** for **SC-004** (text/image swap within one business day after training)
- [x] T034 [P] Update `apps/firm-site/README.md` to state **v1 = TSX pages** under `src/app/`; **MDX** optional later—consistent with [plan.md](./plan.md)
- [x] T035 [P] Add **accessibility** checks: **`@axe-core/playwright`** on home + contact + one inner page **or** **`eslint-plugin-jsx-a11y`** in ESLint; fail CI on **serious** violations on key templates
- [x] T036 Add **internal link** validation for **SC-002**: **Playwright** or small **Node script** that collects same-origin URLs from `content/navigation.json` + **`sitemap.ts`** output and asserts **HTTP 200** (exclude intentional external URLs)

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase                | Depends on                        | Blocks                         |
| -------------------- | --------------------------------- | ------------------------------ |
| Phase 1 Setup        | —                                 | Phase 2                        |
| Phase 2 Foundational | Phase 1                           | US1, US2, US3                  |
| Phase 3 US1          | Phase 2                           | — (MVP shippable content site) |
| Phase 4 US2          | Phase 2 + US1 pages existing      | —                              |
| Phase 5 US3          | Phase 2; benefits from US1 routes | —                              |
| Phase 6 Polish       | US1–US3 desired scope             | —                              |

### User Story Dependencies

- **US1**: Requires Foundational (Phase 2). No dependency on US2/US3.
- **US2**: Best exercised after **US1** routes exist; can overlap with US3 documentation.
- **US3**: Can proceed after Phase 2; health route independent of full content.

### Parallel Opportunities

- **Phase 1**: T003 and T004 after T001–T002 baseline exists.
- **Phase 3 US1**: T012–T016 parallel once T011 establishes patterns; T017 after slugs list is finalized.
- **Phase 6**: T027 and T028 in parallel; after **navigation** + **`sitemap.ts`** exist, **T035** and **T036** in parallel; **T032**–**T034** can overlap with other Phase 6 work.

### Parallel Example: User Story 1

```text
After T011 (home pattern):
T012 [P] about-us || T014 [P] practice-areas || T015 [P] book-online/payment
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1): all routes + images + sitemap.
3. **Stop and validate** with stakeholder walkthrough against reference HTML.

### Incremental Delivery

1. Add Phase 4 (US2) performance hardening and documented Lighthouse profile.
2. Add Phase 5 (US3) extension docs + health + form stub.
3. Polish: Playwright smoke (**T027**), licenses, README/workspace docs, then **T032**–**T036** (usability doc, content workflow, TSX README, **a11y**, full internal links).

### Suggested MVP Scope

- **MVP**: Phases 1–3 (T001–T019) — **FR-001** satisfied for launch review; **SC-002** full internal link pass **after T036** (T027 remains smoke subset).

---

## Notes

- **Booking/payment embeds**: Implement as **iframe** or external links per firm choice—may add tasks when URLs/embed codes are finalized.
- **Task count**: **41** tasks (T001–T041); **T032**–**T036** added for **`/speckit.analyze`** remediation (**SC-003**, **SC-004**, TSX/**MDX** alignment, **a11y**, **SC-002** links); **T037–T041** added to make **FR-006** and **FR-007** explicitly deliverable.
- **Per-story counts**: US1 = 9 tasks (T011–T019), US2 = 4 tasks (T020–T023), US3 = 3 tasks (T024–T026), Setup = 4, Foundational = 6, Polish = **10** (T027–T031, T032–T036).
