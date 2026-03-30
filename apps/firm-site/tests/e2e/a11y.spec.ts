import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const keyPaths = ["/", "/contact-us", "/practice-areas"];

test.describe("accessibility (serious/critical)", () => {
  for (const path of keyPaths) {
    test(`axe on ${path}`, async ({ page }) => {
      await page.goto(path);
      const results = await new AxeBuilder({ page }).analyze();
      const bad = results.violations.filter(
        (v) => v.impact === "serious" || v.impact === "critical",
      );
      expect(bad, bad.map((v) => `${v.id}: ${v.help}`).join("\n")).toEqual([]);
    });
  }
});
