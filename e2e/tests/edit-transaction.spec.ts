import { expect, test } from "@playwright/test";

const today = new Date().toISOString().slice(0, 10);

test("edits an existing transaction", async ({ page }) => {
  // Intercept PUT requests to log errors
  const putResponses: any[] = [];
  page.on('response', (response) => {
    if (response.url().includes('/api/transactions/') && response.request().method() === 'PUT') {
      putResponses.push({ url: response.url(), status: response.status(), body: response.body() });
    }
  });
  // Step 1: Add a new transaction
  await page.goto("/transactions");

  await page.getByTestId("add-transaction-button").click();
  await expect(
    page.getByRole("heading", { name: "Add transaction" }),
  ).toBeVisible();

  await page.getByLabel("Date").fill(today);
  await page.getByLabel("Description").fill("E2E Edit Test");
  await page.getByLabel("Amount (PLN)").fill("100.00");
  await page.getByRole("button", { name: "Add" }).click();

  await page.waitForURL("**/transactions");
  const editRow = page.getByRole('row', { name: 'E2E Edit Test' });
  await expect(editRow).toContainText("100.00 PLN");

  // Step 2: Click edit button
  await editRow.getByTestId('edit-transaction-button').click();
  await expect(
    page.getByRole("heading", { name: "Edit transaction" }),
  ).toBeVisible();

  // Step 3: Change fields
  await page.getByLabel("Description").fill("E2E Edit Test Updated");
  await page.getByLabel("Amount (PLN)").fill("200.50");
  await page.getByLabel("Notes").fill("edited via e2e");

  // Step 4: Save
  await page.getByRole("button", { name: "Save" }).click();

  // Step 5: Verify redirect and updated values
  await page.waitForURL("**/transactions");
  const updatedRow = page.getByRole('row', { name: 'E2E Edit Test Updated' });
  await expect(updatedRow).toContainText("200.50 PLN");
});

test("debug: log PUT errors", async ({ page }) => {
  const putResponses: any[] = [];
  page.on('response', async (response) => {
    if (response.url().includes('/api/transactions/') && response.request().method() === 'PUT') {
      putResponses.push({ url: response.url(), status: response.status(), body: await response.text() });
    }
  });

  await page.goto("/transactions");
  await page.getByTestId("add-transaction-button").click();
  await expect(page.getByRole("heading", { name: "Add transaction" })).toBeVisible();
  await page.getByLabel("Date").fill(today);
  await page.getByLabel("Description").fill("Debug Test");
  await page.getByLabel("Amount (PLN)").fill("100.00");
  await page.getByRole("button", { name: "Add" }).click();
  await page.waitForURL("**/transactions");

  const debugRow = page.getByRole('row', { name: 'Debug Test' });
  await debugRow.getByTestId('edit-transaction-button').click();
  await expect(page.getByRole("heading", { name: "Edit transaction" })).toBeVisible();

  await page.getByLabel("Description").fill("Debug Test Updated");
  await page.getByLabel("Amount (PLN)").fill("200.50");
  await page.getByLabel("Notes").fill("debug");
  await page.getByRole("button", { name: "Save" }).click();

  // Log the PUT response
  console.log('PUT responses:', JSON.stringify(putResponses, null, 2));
});
