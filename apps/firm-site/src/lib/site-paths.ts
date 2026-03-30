import navigation from "../../content/navigation.json";

/** All first-party paths that should return 200 in production (SC-002). */
export function getAllInternalPaths(): string[] {
  const fromNav = [...navigation.header, ...navigation.footer].map(
    (l) => new URL(l.href, "http://local.test").pathname,
  );
  return [...new Set(fromNav)].sort();
}
