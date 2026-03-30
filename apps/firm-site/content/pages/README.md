# Content pages (`content/pages/`)

**v1** uses **TSX** under `src/app/` as the primary source of truth. This folder is reserved for:

- Future **MDX** or **Markdown** files with **frontmatter** (`title`, `description`, `lastReviewed`) aligned with [data-model.md](../../../specs/003-firm-site-replica/data-model.md).
- Optional migration of long-form copy out of TSX when editors need file-based content.

Published page fields map to routes: `slug` ↔ `src/app/**/page.tsx` or a future `content/pages/*.mdx`.
