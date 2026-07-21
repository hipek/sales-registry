import Link from "next/link"
import { formatPLN } from "@/lib/format"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Download, Building2, FileText } from "lucide-react"

interface InvoiceItem {
  description: string
  quantity: number
  unit: string
  unit_price: number
  total: number
}

interface InvoicePreviewProps {
  invoice: {
    invoice_number: string
    issue_date: string
    seller: {
      name: string
      address: string
      nip?: string
    }
    items: InvoiceItem[]
    total: number
  }
  transactionId: string
}

export function InvoicePreview({ invoice, transactionId }: InvoicePreviewProps) {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" asChild>
            <Link href={`/transactions/${transactionId}`}>
              <ArrowLeft className="mr-1 h-4 w-4" /> Powrót
            </Link>
          </Button>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Paragon {invoice.invoice_number}</h1>
            <p className="text-sm text-muted-foreground mt-0.5">
              Sprzedaż nierejestrowana
            </p>
          </div>
        </div>
        <Button size="sm" asChild>
          <a href={`/api/invoices/${transactionId}/download`}>
            <Download className="mr-2 h-4 w-4" /> Pobierz PDF
          </a>
        </Button>
      </div>

      <Card>
        <CardHeader className="border-b bg-muted/30">
          <div className="flex items-center gap-3">
            <Building2 className="h-5 w-5 text-primary" />
            <div>
              <CardTitle className="text-base">{invoice.seller.name}</CardTitle>
              <p className="text-xs text-muted-foreground">{invoice.seller.address}</p>
              {invoice.seller.nip && (
                <p className="text-xs text-muted-foreground">NIP: {invoice.seller.nip}</p>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4 pt-4">
          <div className="flex gap-6 text-sm">
            <div>
              <span className="text-muted-foreground">Paragon nr:</span>{" "}
              <strong className="tabular-nums">{invoice.invoice_number}</strong>
            </div>
            <div>
              <span className="text-muted-foreground">Data wystawienia:</span>{" "}
              <strong>{invoice.issue_date}</strong>
            </div>
          </div>

          <div className="rounded-lg border">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-muted/30">
                  <th className="px-4 py-2.5 text-left font-medium text-muted-foreground">Towar/usługa</th>
                  <th className="px-4 py-2.5 text-right font-medium text-muted-foreground">Ilość</th>
                  <th className="px-4 py-2.5 text-right font-medium text-muted-foreground">Cena jedn.</th>
                  <th className="px-4 py-2.5 text-right font-medium text-muted-foreground">Razem</th>
                </tr>
              </thead>
              <tbody>
                {invoice.items.map((item, i) => (
                  <tr key={i} className="border-b last:border-0">
                    <td className="px-4 py-2.5">{item.description}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums">{item.quantity} {item.unit}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums">{formatPLN(item.unit_price)}</td>
                    <td className="px-4 py-2.5 text-right font-semibold tabular-nums">{formatPLN(item.total)}</td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr className="border-t bg-muted/20">
                  <td colSpan={3} className="px-4 py-3 text-right text-sm font-semibold">RAZEM:</td>
                  <td className="px-4 py-3 text-right text-base font-bold tabular-nums text-primary">
                    {formatPLN(invoice.total)}
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>

          <div className="flex items-center gap-2 text-xs text-muted-foreground border-t pt-3">
            <FileText className="h-3.5 w-3.5" />
            Paragon wystawiony dla działalności nierejestrowanej — bez NIP nabywcy
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
