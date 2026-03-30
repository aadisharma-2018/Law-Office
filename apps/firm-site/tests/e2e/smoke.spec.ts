import { test, expect } from "@playwright/test";

test.describe("smoke", () => {
  test("home, contact, booking load without console errors", async ({
    page,
  }) => {
    const errors: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "error") errors.push(msg.text());
    });

    await page.goto("/");
    expect(page).toHaveURL("/");
    await expect(
      page.getByRole("heading", { name: /Immigration Attorney/i }),
    ).toBeVisible();

    await page.goto("/contact-us");
    await expect(
      page.getByRole("heading", { name: /Contact us/i }),
    ).toBeVisible();

    await page.goto("/book-online");
    await expect(
      page.getByRole("heading", { name: /Book online/i }),
    ).toBeVisible();

    expect(errors, `console errors: ${errors.join("; ")}`).toEqual([]);
  });
});
