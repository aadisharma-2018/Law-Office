/** Services (used for display / future booking options). */
export const SERVICES: { slug: string; title: string; summary: string }[] = [
  {
    slug: "review-one-document",
    title: "Review one document",
    summary:
      "Attorney review of a single immigration-related document with written guidance.",
  },
  {
    slug: "10-minute-phone-consultation",
    title: "10 minute phone consultation",
    summary: "Short phone session to address a focused immigration question.",
  },
  {
    slug: "15-minute-phone-consultation",
    title: "15 minute phone consultation",
    summary: "Phone consultation for brief case guidance.",
  },
  {
    slug: "20-minute-phone-consultation",
    title: "20 minute phone consultation",
    summary: "Extended phone consultation for multiple questions.",
  },
  {
    slug: "30-minute-phone-consultation",
    title: "30 minute phone consultation",
    summary: "In-depth phone consultation for strategy and planning.",
  },
  {
    slug: "in-office-consultation",
    title: "In Office consultation",
    summary: "Meet in person to discuss your immigration matter.",
  },
  {
    slug: "review-one-uscis-form",
    title: "Review one USCIS form",
    summary: "Line-by-line review of a single USCIS form before filing.",
  },
  {
    slug: "review-one-entire-application",
    title: "Review one entire application",
    summary: "Comprehensive review of a full application package.",
  },
  {
    slug: "other-immigration-filings",
    title: "Other Immigration filings",
    summary: "Support for additional filings not listed separately.",
  },
  {
    slug: "review-of-criminal-file",
    title: "Review of criminal file",
    summary: "Assessment of criminal history for immigration consequences.",
  },
  {
    slug: "review-rfe-noid-denial-advise",
    title: "Review RFE, NOID, Denial & advise",
    summary: "Guidance on government notices and next steps.",
  },
  {
    slug: "next-day-follow-up-phone-consultation",
    title: "Next day Follow up phone consultation",
    summary: "Follow-up call after a prior consultation.",
  },
];

export const SERVICE_SLUGS = SERVICES.map((s) => s.slug);

export function getService(slug: string) {
  return SERVICES.find((s) => s.slug === slug);
}
