# Feature Specification: Rebuild firm public website from reference materials (performance-ready)

**Feature Branch**: `003-firm-site-replica`  
**Created**: 2026-03-29  
**Status**: Draft  
**Input**: User description: "I have copied all html pages of www.lawyersharma.com. Since I do not have access to the code base, I would like to replicate this website and add more functionality at a later point. Suggest best tech stack for building the website, website has to be fast performant"

## Clarifications

### Session 2026-03-29

- Q: Who owns the public site content and may implementers mirror images and CSS for the rebuild? → A: The firm **owns the website and all of its contents**, including **images**. Implementers **may download images and other CSS** (and related static assets) from the authoritative sources for use when building the replacement site, alongside the saved HTML reference set.
- Q: Must the new site be a pixel-perfect copy of the live site, or may styling use other sources? → A: **Exact duplication is not required.** **www.lawyersharma.com** is a **reference** for information architecture, content, and brand intent. Implementers **may use open-source CSS**, component libraries, design systems, and similar **openly licensed** assets **instead of** reusing legacy builder CSS wholesale, subject to **license compliance** and firm approval of overall look-and-feel.
- Q: Remediation for `/speckit.analyze` (G1–G5: SC-003/SC-004 coverage, MDX vs TSX alignment, a11y checks, SC-002 link coverage)? → A: **SC-003** and **SC-004** are evidenced by **documented** usability and **content workflow** artifacts per **`tasks.md`** (T032, T033). **v1** **primary** pages are **TSX** in the Next.js App Router; **MDX** remains **optional** for a later increment (**`plan.md`**). **Accessibility** automated checks and **internal link** crawling for **SC-002** are **tasks** T035 and T036.

### Session 2026-03-30

- Q: Where should the 002 USCIS prefill tool live when converted to JavaScript? → A: Not public-facing; **staff-only** internal tool (web) integrated into the Next.js site.
- Q: How should staff access be enforced for the USCIS prefill tool? → A: Defer “client portal + RBAC” authentication/authorization details to a **future** feature spec (this spec only states staff-only + access-controlled).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visitors see an equivalent public site (Priority: P1)

Prospective clients, referrers, and the public open the firm’s **replacement** public website and find **equivalent** primary content compared to the **reference** set (structure, key messaging, contact paths, practice descriptions, and legal notices such as terms/disclaimer where applicable). **Visual design** may differ from the legacy site if the new presentation remains **professional**, **on-brand**, and meets accessibility/performance goals. Navigation between main sections is **clear** and does not strand users on broken links for pages that existed in the reference set.

**Why this priority**: The site is the firm’s storefront; alignment with the reference **content and journeys** reduces confusion and preserves lead-generation paths without blocking a **modern** implementation stack.

**Independent Test**: Using a checklist derived from the archived pages, walk each major route (home, about, practice areas, contact, booking-related entry points, payment, policies) and confirm content intent and calls-to-action are present and correct.

**Acceptance Scenarios**:

1. **Given** a visitor opens the home page, **When** they scan headings and hero content, **Then** they recognize the same firm positioning and primary calls-to-action as in the reference materials (allowing normal copy edits).
2. **Given** a visitor uses primary navigation, **When** they open each top-level section that existed in the reference, **Then** they reach a page that fulfills the same purpose without dead ends for those routes.
3. **Given** a visitor needs to contact the firm, **When** they follow the contact path from the reference design intent, **Then** they can complete contact or scheduling flows the firm chooses to support in v1.

---

### User Story 2 - Site feels fast and works on phones (Priority: P1)

Typical visitors on **mobile and desktop** experience **perceived speed** that meets **SC-001** (above-the-fold meaningful content within the **documented** time budget on a defined network profile). The experience remains usable on common phone sizes without horizontal scrolling for main reading columns.

**Why this priority**: Performance and mobile usability directly affect trust, SEO, and conversion for professional services sites.

**Independent Test**: Measure representative pages under controlled conditions (lab or field) against the success criteria for perceived speed; smoke-test on one iOS and one Android browser size.

**Acceptance Scenarios**:

1. **Given** a first-time visitor on a median mobile connection, **When** they load a primary content page, **Then** meaningful text or imagery appears within the time budget in the success criteria (not a blank screen).
2. **Given** a visitor rotates the device or resizes the window, **Then** layout remains readable without breaking core navigation.

---

### User Story 3 - Firm can extend the site later without starting over (Priority: P2)

The firm’s maintainers can add **new** pages or capabilities (for example: intake tools, client resources, or integrations) **without** replacing the entire front door again, within normal product evolution.

**Why this priority**: The motivation to leave a proprietary builder is partly future flexibility; the first delivery should not paint the firm into a corner.

**Independent Test**: Document extension points (e.g. where new routes, modules, or services plug in) and run a tabletop exercise: “add one new authenticated staff-only page” without re-platforming.

**Acceptance Scenarios**:

1. **Given** the firm approves a new feature that belongs on the public site, **When** implementers follow the documented extension approach, **Then** they can add it with bounded risk to existing pages.
2. **Given** content editors update text or images on marketing pages, **When** they publish, **Then** they do not need a full redeploy of unrelated sections for routine edits (per the chosen operating model in planning).

---

### Edge Cases

- **Reference HTML is not a full app**: Archived “page source” from a hosted builder may omit client-rendered content; the rebuild may require **content authoring** or **design extraction**, not only copying files.
- **Styling is not locked to legacy CSS**: The new site **may** use **open-source** CSS, frameworks, or component libraries; the live site remains a **reference** for layout/content intent, not mandatory stylesheet reuse.
- **Assets and third parties**: **Firm-owned** images (and optional legacy CSS as **reference**) may be **mirrored** into reference materials. **Third-party** embeds (schedulers, analytics, payment widgets, CDNs) may still be **licensed or domain-bound**; those integrations need separate review and failure handling.
- **Booking/commerce**: Service and payment flows may depend on **external** schedulers or processors; v1 may **link out** or re-embed per compliance review.
- **SEO and URLs**: Changing domains or paths affects search; redirects or a URL plan may be required when replacing the live site.
- **Accessibility**: Legacy markup may not meet current accessibility expectations; remediation may change structure while preserving intent.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The delivered public site MUST implement **equivalent** **information architecture** and **primary user journeys** to the firm’s **reference page set** (saved HTML and **reference asset bundle** where used—see **FR-008**), except where deliberately updated in writing by the firm. **Visual styling** need not match the legacy site pixel-for-pixel.
- **FR-002**: The site MUST meet **stated performance targets** in the Success Criteria for **key** pages (home, contact, primary practice entry).
- **FR-003**: The site MUST be **usable on mobile** and **desktop** at common viewport widths without breaking core reading and navigation.
- **FR-004**: The firm MUST be able to **update** marketing/legal copy and imagery through a defined process (self-serve editor, CMS, or agreed handoff) without requiring specialized-only knowledge unless explicitly accepted by the firm.
- **FR-005**: The solution MUST separate **public marketing** concerns from **sensitive client operations** so future features (portals, document exchange) can be added with **appropriate** access control when scoped.
- **FR-006**: The firm MUST receive **guidance** on **hosting, domain, HTTPS, backups, and privacy/disclosure** obligations for the new property before launch (content of guidance in planning/operations, not this spec).
- **FR-007**: Where forms or scheduling exist, submissions MUST follow the firm’s **data-handling** rules (notice, consent where required, retention, least data collected).
- **FR-008**: The firm **authorizes** use of **firm-owned** static assets—including **images** and, as needed, **legacy stylesheets**—collected from authoritative sources for **reference**, brand continuity, and migration. The implementation **may** substitute **open-source** CSS, component libraries, or design systems **instead of** reusing legacy CSS wholesale. An inventory of **which** assets and **open-source** dependencies are relied upon in the build MUST be maintainable for updates, audits, and **license** compliance (exact storage mechanism is planning detail).
- **FR-009**: All **open-source** or third-party **styles**, **components**, and **libraries** used in the public site MUST be incorporated in compliance with their **license terms** and the firm’s policies (e.g. attribution, notice files where required).

### Key Entities

- **Reference page set**: Archived HTML used as the **content and structure** baseline; **www.lawyersharma.com** is a **reference**, not a mandate to duplicate implementation details.
- **Reference asset bundle**: Firm-owned **images**, optional **legacy CSS** for reference, **web fonts**, and other static files mirrored or exported to support the rebuild; may be **partially superseded** by **open-source** styling in the delivered site.
- **Published page**: A routable page on the new site with content role (marketing, policy, service description, etc.).
- **Navigation model**: Top-level and footer links and how users move between sections.
- **Media asset**: Images and files used in the public site; **firm-owned** materials are cleared for reuse in the rebuild; optimize for performance where applicable.
- **Extension**: A future capability (e.g. client login, tools) scoped outside minimal replication unless the firm promotes it to v1.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On **key pages**, representative tests show **above-the-fold** meaningful content available within **3 seconds** on a **defined** “typical” mobile network profile used for acceptance (documented with the test plan—not vendor-specific tooling in this spec).
- **SC-002**: **Zero** critical broken links within the **scoped** navigation map derived from the reference set at launch (excluding third-party URLs the firm intentionally retires).
- **SC-003**: **90%** of usability-test participants complete “find contact information” and “find practice focus” tasks on first attempt without moderator intervention in structured tests with **at least five** participants.
- **SC-004**: The firm’s **maintainers** can perform a documented **routine content edit** (text/image swap on one page) within **one business day** of training, without emergency developer involvement, unless the firm opts for a fully vendor-managed model (then document SLA instead).

### Success criteria — validation traceability

Evidence for **SC-001**–**SC-004** is produced during implementation: **lab/CI** performance and **link** checks (**SC-001**, **SC-002**), **moderated usability** script and results or **approved deferral** (**SC-003**), and **documented** update workflow plus **dry-run** (**SC-004**). Concrete steps are listed in **`tasks.md`** (including post-analyze tasks **T032**–**T036**).

## Assumptions

- The firm **owns the website and its contents**, including **images**, and authorizes mirroring **images and CSS** (and related static assets) for the rebuild; **third-party** scripts/embeds remain subject to their own terms and firm policy.
- **Rebuild** targets **equivalent** user-visible **content** and **journeys** using the current public site as **reference**; **pixel-perfect** or stylesheet-level identity with the legacy builder is **not** required. **Open-source** CSS and similar assets **may** be used; **FR-009** applies to license obligations.
- **Technology selection** (frameworks, hosting vendor, CMS shape) is **out of scope** for this specification and belongs in **implementation planning**, subject to meeting **FR-002** and maintainability goals.
- **Performance** will be validated with **repeatable** tests agreed during planning (lab metrics and/or real-user monitoring), not ad hoc subjective opinion alone.
- **Client-confidential** workflows remain **out of scope** for v1 unless explicitly added; the public site may **link** to separate tools under a future specification.
- The USCIS prefill POC (002) is intended to be reimplemented in JavaScript as a **staff-only** web tool integrated into the same Next.js codebase (access-controlled), not exposed as a public marketing route by default.
