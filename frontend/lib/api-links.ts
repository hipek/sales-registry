export function transactionCsvUrl(): string {
  return "/api/transactions/export"
}

export function invoicePdfUrl(transactionId: string): string {
  return `/api/invoices/${transactionId}/download`
}
