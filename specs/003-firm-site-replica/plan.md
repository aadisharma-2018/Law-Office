# Implementation Plan: Rebuild firm public website from reference materials (performance-ready)

**Branch**: `003-firm-site-replica` | **Date**: 2026-03-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/003-firm-site-replica/spec.md`

## Summary

Rebuild **www.lawyersharma.com** as a **firm-owned**, **fast** marketing site using **reference** HTML and assets under `documents/lawyersharma-com/` plus firm-approved images/CSS. **No pixel-perfect** Wix clone (**spec** clarifications): **equivalent** information architecture, content, and journeys; **open-source** styling (e.g. **Tailwind CSS**) and components are allowed (**FR-008**, **FR-009**).

**Chosen approach (Phase 0):** **Next.js** (App Router) + **TypeScript** + **Tailwind CSS**, deployed to a **global edge CDN** (e.g. **Vercel**). **v1 primary** marketing pages are implemented as **`page.tsx` (TSX)** under `src/app/` for speed of delivery and alignment with **`tasks.md`**; **MDX** (or **markdown**) in `content/` is **optional** and can be introduced for selected routes or a later increment (**FR-004**). **next/image** for optimized images from the **reference asset bundle**. Performance validated against **SC-001** (e.g. Lighthouse + **4G** throttling profile documented in the test plan).

**Relationship to other repos:** Existing **`apps/uscis-fill-local`** remains a **separate** tool; the public site may **link** to it or future portals (**FR-005**, **spec** assumptions).

## Technical Context

**Language/Version**: **TypeScript 5.x**, **Node.js 20 LTS**  
**Primary Dependencies**: **Next.js** (App Router), **React**, **Tailwind CSS**; **optional** **MDX** later (`@next/mdx` or `next-mdx-remote`); **next/font** for web fonts; **ESLint** + **Prettier**; **@axe-core/playwright** (or **eslint-plugin-jsx-a11y**) for accessibility checks per **tasks**  
**Storage**: **Git-tracked** content (TSX pages + `content/navigation.json` + optional future MDX); **no** firm client/matter database for v1 public site. Form leads optional: **serverless** handler + **email** or **CRM** webhook (planning detail).  
**Testing**: **Playwright** (smoke + critical paths per **SC-002**/**SC-003**); **Lighthouse CI** or **@lhci/cli** for performance budgets vs **SC-001**; a11y spot-checks (**axe**) for key templates  
**Target Platform**: **Modern browsers**; **responsive** mobile/desktop (**FR-003**)  
**Project Type**: **Web application** (static-first + SSR/ISR where needed)  
**Performance Goals**: Meet **SC-001** on key routes; **Core Web Vitals** in “green” band on lab tests for home/contact/practice entry; **image** and **font** optimization mandatory  
**Constraints**: **HTTPS** only in production; **secrets** (API keys, SMTP) via env only; **FR-009** license/attribution for OSS; **privacy** copy and form handling per **FR-007**  
**Scale/Scope**: **Marketing** site; low–moderate traffic; **~dozen** top-level routes mirroring sitemap-derived reference  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence in this plan |
|-----------|--------|------------------------|
| **I. Confidentiality & data minimization** | Pass | Public marketing only; **contact/lead** forms collect **minimum** fields; submissions **not** logged with full PII in client-side analytics; env-based secrets; no client matter data in v1 scope ([spec.md](./spec.md)). |
| **II. Spec-driven delivery** | Pass | Plan and artifacts trace to [spec.md](./spec.md) FR/US/SC; stack choices support **FR-002**–**FR-009**. |
| **III. Auditability** | Pass | Server-side form handlers (when added) log **metadata** (timestamp, route)—not full message body in application logs if policy requires; CRM/webhook as system of record optional. |
| **IV. Testing discipline** | Pass | [research.md](./research.md) §9 + Playwright/Lighthouse for acceptance-aligned checks. |
| **V. Simplicity** | Pass | **Single** Next.js app; **no** extra services until a feature needs them; see [Complexity Tracking](#complexity-tracking). |

**Post–Phase 1 re-check:** Pass — no change to gates.

## Project Structure

### Documentation (this feature)

```text
specs/003-firm-site-replica/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── README.md
└── spec.md
```

### Source Code (repository root) — proposed

```text
apps/firm-site/                    # new Next.js app (name may be adjusted)
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── content/                       # MDX/MD pages (or mdx under src/)
│   ├── pages/
│   └── navigation.json            # optional: nav model
├── public/
│   └── images/                    # optimized assets from reference bundle
├── src/
│   ├── app/                       # App Router layouts, pages, loading/error
│   ├── components/
│   └── lib/                       # helpers, metadata, analytics wrapper
└── tests/
    └── e2e/                       # Playwright

documents/lawyersharma-com/        # existing HTML snapshots (reference only)
```

**Structure Decision**: **One** Next.js application under **`apps/firm-site/`** (or `web/lawyersharma/` if the monorepo prefers `web/`). Keeps parity with [workspace rules](../../.cursor/rules/specify-rules.mdc) `backend/frontend/` style if adopted; otherwise `apps/` is fine. **Reference** HTML stays in **`documents/`**; **not** served verbatim as production HTML.

## Complexity Tracking

_No unjustified violations._ Optional **headless CMS** or **separate** API service deferred until **FR-004** editing model requires it.

| Addition | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|-------------------------------------|
| Next.js vs plain static | Future routes, APIs, auth (**US3**); image/font optimization | Raw HTML folder cannot meet maintainability and **SC-001** as cleanly |

---

## Phase 0: Outline & Research

**Output:** [research.md](./research.md)

Consolidated decisions: **Next.js + Tailwind + MDX**, hosting, content workflow, performance testing, third-party embeds (booking/analytics), OSS license hygiene (**FR-009**).

## Phase 1: Design & Contracts

**Outputs:**

- [data-model.md](./data-model.md) — content entities (pages, nav, media), not a transactional DB
- [contracts/](./contracts/) — public site boundaries; README describes HTTP surface and future form contract
- [quickstart.md](./quickstart.md) — install, dev server, env vars, performance smoke commands

**Agent context:** Run `.specify/scripts/bash/update-agent-context.sh cursor-agent`.

## Phase 2

Implementation tasks are **not** produced by `/speckit.plan`. Run **`/speckit.tasks`** when ready.

---

## Subprocessors & data flows (public marketing)

| System | Flow |
|--------|------|
| **Hosting / CDN** (e.g. Vercel) | Serves pages and static assets; may process **server actions** / form posts. |
| **Analytics** (optional) | Page views; configure to **avoid** unnecessary PII; disclose in privacy policy. |
| **Booking / payments** (Wix or other) | **Embed** or **link** per firm choice; data governed by third-party terms (**spec** edge cases). |
| **Email / CRM** (optional) | Contact form delivery; subprocessors listed in privacy notice. |

Review DPAs/terms for any **third-party** that receives **lead** or **client** data.
