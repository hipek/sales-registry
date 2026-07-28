import { expect, test } from "@playwright/test";

const today = new Date().toISOString().slice(0, 10);

test("adds a new item to the sales list", async ({ page }) => {
  await page.goto("/transactions");

  await page.getByTestId("add-transaction-button").click();
  await expect(
    page.getByRole("heading", { name: "Add transaction" }),
  ).toBeVisible();

  await page.getByLabel("Date").fill(today);
  await page.getByLabel("Description").fill("E2E test item");
  await page.getByLabel("Amount (PLN)").fill("100.00");
  await page.getByRole("button", { name: "Add" }).click();

  await page.waitForURL("**/transactions");
  await expect(page.getByTestId("transaction-row")).toContainText(
    "E2E test item",
  );
  await expect(page.getByTestId("transaction-row")).toContainText("100.00 PLN");
});
