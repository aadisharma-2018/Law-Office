# Research: Rebuild firm public website (reference-based)

**Branch**: `003-firm-site-replica`  
**Date**: 2026-03-29  
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

Consolidated technology and process decisions for Phase 0. Resolves “best stack for **fast**, **extensible** marketing site” from the original feature ask, within **FR-008**/**FR-009** and clarifications (reference-only, OSS styling allowed).

---

## 1. Application framework

| Item | Decision |
|------|----------|
| **Decision** | **Next.js** (App Router), **TypeScript**, **React 18+**. |
| **Rationale** | **Static generation** + **ISR** for fast global delivery; **built-in** image/font optimization; **API routes** / **Server Actions** for future forms and integrations without a second backend for simple cases; large ecosystem; aligns with common **law firm** and **agency** patterns. |
| **Alternatives considered** | **Astro** (excellent for content-only; weaker if the firm soon adds **auth**/dashboard on same domain). **Remix** (strong UX; slightly different hosting defaults). **Plain Vite + React** (more manual routing/SEO/SSR). |

---

## 2. Styling and UI

| Item | Decision |
|------|----------|
| **Decision** | **Tailwind CSS** + **headless** patterns; optional **Radix UI** / **shadcn/ui** for accessible primitives (MIT-style licenses—verify **FR-009**). |
| **Rationale** | **Utility-first** matches “open-source CSS” intent; **small** runtime CSS when purged; **accessible** components reduce legal-site a11y risk. Legacy Wix CSS used only as **visual reference**, not shipped wholesale. |
| **Alternatives considered** | **Bootstrap** (heavier bundle). **CSS Modules** only (slower iteration for marketing pages). |

---

## 3. Content management (v1)

| Item | Decision |
|------|----------|
| **Decision** | **Primary:** **TSX** pages under **`src/app/`** (Next.js App Router) for v1 delivery, with **`content/navigation.json`** for nav. **Optional later:** **MDX** or **Markdown** in **`content/`** for selected pages when editors want file-based content (**FR-004**); **frontmatter** for title, description, OG when MDX is adopted. |
| **Rationale** | Aligns **`tasks.md`** implementation with **`plan.md`** after **`/speckit.analyze`**; fastest path to **SC-001**/**SC-002**; **MDX** can be layered without re-platforming. |
| **Alternatives considered** | **MDX-first** for v1 (rejected for this increment to avoid plan vs tasks mismatch). **Sanity** / **Contentful** (add when **SC-004** demands non-dev edits weekly). |

---

## 4. Hosting and performance

| Item | Decision |
|------|----------|
| **Decision** | **Vercel** (or **Netlify** / **Cloudflare Pages**) with **automatic HTTPS**, **CDN**, **preview** deployments per PR. |
| **Rationale** | Meets **SC-001** targets when combined with **next/image**, **font** subsetting, and **minimal** client JS on marketing routes. |
| **Alternatives considered** | **Self-hosted Node** (more ops). **S3 + CloudFront** static only (more work for SSR/forms). |

---

## 5. Images and assets

| Item | Decision |
|------|----------|
| **Decision** | Copy **firm-owned** images into **`public/images`** (or `src/assets`); run through **`next/image`** with explicit **width/height**; **WebP/AVIF** where supported. |
| **Rationale** | **FR-008**; **LCP** improvement vs raw `<img>` from snapshots. |
| **Alternatives considered** | External **CDN** URLs only (adds third-party dependency and caching complexity). |

---

## 6. Forms, privacy, and third-party embeds

| Item | Decision |
|------|----------|
| **Decision** | **Server Action** or **Route Handler** POST for contact forms; **validate** inputs; send via **transactional email** (e.g. Resend, SES) or **CRM** webhook; **reCAPTCHA** or **Turnstile** if spam is an issue. **Privacy policy** and **cookie** banner if analytics/marketing pixels added. |
| **Rationale** | **FR-007** data-handling; **constitution** data minimization. |
| **Alternatives considered** | **Formspree** / **Getform** (faster MVP; another subprocessor to list). |

---

## 7. SEO and URLs

| Item | Decision |
|------|----------|
| **Decision** | **`metadata` API** / MDX frontmatter for titles and descriptions; **`sitemap.ts`** and **`robots.ts`** in App Router; **301** plan documented when **cutting over** from Wix URLs (**spec** edge case). |
| **Rationale** | Professional services rely on **local** and **branded** search. |

---

## 8. Testing strategy

| Boundary | Approach |
|----------|----------|
| **Navigation / links** | **Playwright**: crawl internal links on build artifact; assert **no 404** on scoped map (**SC-002**). |
| **Performance** | **Lighthouse** (CI): **LCP**, **CLS**, **INP** budgets tied to **SC-001** profile (document throttle). |
| **Accessibility** | **axe** in Playwright on home + contact + one inner page. |
| **Visual** | Optional **Percy/Chromatic** later—not required v1. |

---

## 9. Open-source license compliance (FR-009)

| Item | Decision |
|------|----------|
| **Decision** | Maintain **`THIRD_PARTY_NOTICES.md`** or **npm** `license-checker` output in repo; retain **copyright** headers where licenses require; **shadcn**/Radix are typically MIT—confirm per package at install time. |
| **Rationale** | Defensible for firm **IP** and vendor audits. |

---

## Open items (non-blocking for plan; resolve during implementation)

- Exact **booking** embed (Wix Bookings vs **Cal.com** vs link-out).
- **Analytics**: Plausible / GA4 / none—**privacy** copy depends on choice.
- **Domain** cutover runbook (DNS, **SSL**, **redirects** from old Wix subpaths).
