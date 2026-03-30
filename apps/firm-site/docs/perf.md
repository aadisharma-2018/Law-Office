# Performance validation (SC-001)

## Lab profile

Use **Chrome DevTools** → **Lighthouse** (or `npm run lhci` after `npm run build && npm run start`) with:

- **Device**: Mobile or Desktop (document which you use for sign-off).
- **Network**: **Slow 4G** (or Lighthouse “Simulated throttling” with equivalent RTT/throughput).
- **URLs**: `/`, `/contact-us`, `/practice-areas`.

## Targets (adjust with firm)

- **LCP**: Meaningful hero or H1 paint on key routes within the budget agreed in **SC-001** (record the numeric threshold in release notes when the firm signs off).
- **CLS**: Near zero on templates using `next/image` with explicit dimensions where possible.

## Commands

```bash
npm run build && npm run start
# Other terminal:
npm run lhci
```

Document the **exact** Lighthouse version and throttle preset in PRs that claim SC-001.
