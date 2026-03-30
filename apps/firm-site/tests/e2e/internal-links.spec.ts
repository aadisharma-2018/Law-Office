import { test, expect } from "@playwright/test";
import { getAllInternalPaths } from "../../src/lib/site-paths";

/** SC-002: same-origin routes from navigation return 200. */
test("internal paths return 200", async ({ request }) => {
  const paths = getAllInternalPaths();
  expect(paths.length).toBeGreaterThan(5);

  for (const path of paths) {
    const res = await request.get(path);
    expect.soft(res.status(), path).toBe(200);
  }
});
