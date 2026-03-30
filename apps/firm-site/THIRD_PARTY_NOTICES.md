# Third-party notices (FR-009)

This application depends on open-source packages distributed under the licenses listed in each package’s `node_modules/<name>/package.json` (field `"license"`).

Representative runtime and tooling dependencies include:

| Package              | Typical license |
| -------------------- | --------------- |
| next                 | MIT             |
| react                | MIT             |
| tailwindcss          | MIT             |
| typescript           | Apache-2.0      |
| eslint               | MIT             |
| @playwright/test     | Apache-2.0      |
| @axe-core/playwright | MPL-2.0         |
| @lhci/cli            | Apache-2.0      |

Generate a full inventory for audits:

```bash
npx license-checker --production --csv > licenses.csv
```

Review `licenses.csv` before distribution and retain with the firm’s OSS compliance records.
