import Link from "next/link"
import { formatPLN } from "@/lib/format"
import { formatDate } from "@/lib/date"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, FileText, Edit, Download } from "lucide-react"

interface TransactionDetailProps {
  transaction: {
    id: string
    date: string
    description: string
    amount: number
    invoice_number?: string
    notes?: string
  }
}

export function TransactionDetail({ transaction }: TransactionDetailProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" asChild>
          <Link href="/transactions">
            <ArrowLeft className="mr-2 h-4 w-4" /> Powrót
          </Link>
        </Button>
        <h1 className="text-2xl font-bold">Szczegóły transakcji</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{transaction.description}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <dt className="text-sm text-muted-foreground">Data</dt>
              <dd className="font-medium">{formatDate(transaction.date)}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">Kwota</dt>
              <dd className="font-medium">{formatPLN(transaction.amount)}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">Nr paragona</dt>
              <dd className="font-medium">{transaction.invoice_number || "—"}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">Notatki</dt>
              <dd className="font-medium">{transaction.notes || "—"}</dd>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="flex gap-2">
        <Button asChild>
          <Link href={`/invoices/${transaction.id}`}>
            <FileText className="mr-2 h-4 w-4" /> Paragon
          </Link>
        </Button>
        <Button variant="outline" asChild>
          <Link href={`/transactions/${transaction.id}/edit`}>
            <Edit className="mr-2 h-4 w-4" /> Edytuj
          </Link>
        </Button>
      </div>
    </div>
  )
}
