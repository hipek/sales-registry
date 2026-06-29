import Link from "next/link"
import { formatPLN } from "@/lib/format"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Download } from "lucide-react"

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
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" asChild>
            <Link href={`/transactions/${transactionId}`}>
              <ArrowLeft className="mr-2 h-4 w-4" /> Powrót
            </Link>
          </Button>
          <h1 className="text-2xl font-bold">Paragon {invoice.invoice_number}</h1>
        </div>
        <Button asChild>
          <a href={`/api/invoices/${transactionId}/download`}>
            <Download className="mr-2 h-4 w-4" /> Pobierz PDF
          </a>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{invoice.seller.name}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="text-sm text-muted-foreground">{invoice.seller.address}</div>
          {invoice.seller.nip && (
            <div className="text-sm">NIP: {invoice.seller.nip}</div>
          )}
          <div className="text-sm">
            Paragon nr: <strong>{invoice.invoice_number}</strong>
          </div>
          <div className="text-sm">
            Data wystawienia: <strong>{invoice.issue_date}</strong>
          </div>

          <div className="border-t pt-4 mt-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2">Towar/usługa</th>
                  <th className="text-right py-2">Ilość</th>
                  <th className="text-right py-2">Cena jedn.</th>
                  <th className="text-right py-2">Razem</th>
                </tr>
              </thead>
              <tbody>
                {invoice.items.map((item, i) => (
                  <tr key={i} className="border-b">
                    <td className="py-2">{item.description}</td>
                    <td className="text-right">{item.quantity} {item.unit}</td>
                    <td className="text-right">{formatPLN(item.unit_price)}</td>
                    <td className="text-right font-medium">{formatPLN(item.total)}</td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr className="font-bold">
                  <td colSpan={3} className="py-2 text-right">RAZEM:</td>
                  <td className="text-right">{formatPLN(invoice.total)}</td>
                </tr>
              </tfoot>
            </table>
          </div>

          <div className="text-xs text-muted-foreground pt-4">
            Sprzedaż nierejestrowana — paragon bez NIP nabywcy
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
