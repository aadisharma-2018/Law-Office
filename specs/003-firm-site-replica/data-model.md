# Data Model: Rebuild firm public website (reference-based)

**Branch**: `003-firm-site-replica`  
**Date**: 2026-03-29  
**Spec**: [spec.md](./spec.md)

## Overview

The public marketing site is **content-centric**: there is **no** client/matter database in v1. Persisted data are **files in Git** (MDX/Markdown, images, config) plus optional **runtime** records if forms write to email/CRM (out of band for this model).

---

## Entities

### Published page

A routable URL with marketing or policy content.

| Field | Type | Notes |
|-------|------|--------|
| `slug` | string | URL path segments, e.g. `contact-us`, `book-online` |
| `title` | string | `<title>` and H1 default |
| `description` | string | Meta description / OG |
| `contentType` | enum | `mdx`, `markdown`, `tsx` (custom page) |
| `lastReviewed` | date | Optional; for legal pages |
| `status` | enum | `draft`, `published` (if using preview workflow) |

**Uniqueness:** one `slug` per deployed site version.

---

### Navigation model

Top-level and footer links (**spec** Key Entity).

| Field | Type | Notes |
|-------|------|--------|
| `id` | string | Stable id for reordering |
| `label` | string | Display text |
| `href` | string | Internal path or external URL |
| `placement` | enum | `header`, `footer`, `mobile` |
| `order` | number | Sort order |

---

### Reference page set (read-only)

Archived HTML under `documents/lawyersharma-com/` — **not** the runtime schema; used for **content parity** checks during migration.

| Field | Type | Notes |
|-------|------|--------|
| `sourceFile` | string | e.g. `index.html` |
| `notes` | string | Gaps vs rendered Wix (JS-only content) |

---

### Reference asset bundle

Firm-owned **images**, optional **legacy CSS** for designer reference, **fonts**.

| Field | Type | Notes |
|-------|------|--------|
| `path` | string | Repo path under `public/` or `assets/` |
| `kind` | enum | `image`, `stylesheet`, `font`, `other` |
| `license` | string | `firm-owned` or SPDX id for OSS |
| `usedInProduction` | boolean | False if reference-only |

---

### Media asset (published)

Optimized image or file **served** from the new site.

| Field | Type | Notes |
|-------|------|--------|
| `id` | string | Stable id for MDX |
| `src` | string | Path to optimized file |
| `alt` | string | Required for images; **a11y** |
| `width` / `height` | number | For **CLS** control |

---

### Lead submission (optional, when forms exist)

If contact forms are implemented:

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Server-generated |
| `submittedAt` | datetime | |
| `route` | string | Page slug where form posted |
| `payload` | JSON | **Minimize** PII; encrypt at rest if stored |

**Rule:** Prefer **forwarding** to email/CRM **without** long-term DB storage unless the firm requires an audit trail (**constitution**).

---

## Validation rules (from spec)

- **FR-001**: Every **published** `slug` maps to a **purpose** in the reference navigation map unless explicitly retired.
- **FR-009**: Every **OSS** dependency has a **license** entry in build metadata.
- **FR-007**: Forms capture only fields **shown** in the privacy notice; retention documented.

---

## State transitions

**Published page**: `draft` → `published` (optional if using preview-only workflow).

No complex lifecycle for v1 marketing content beyond Git workflow (PR → merge → deploy).
