import Link from "next/link"
import { formatPLN } from "@/lib/format"
import { formatDate } from "@/lib/date"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  ArrowLeft,
  FileText,
  Edit,
  Calendar,
  Tag,
  FileDigit,
  StickyNote,
} from "lucide-react"

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
  const details = [
    { icon: Calendar, label: "Date", value: formatDate(transaction.date) },
    {
      icon: Tag,
      label: "Amount",
      value: formatPLN(transaction.amount),
      highlight: true,
    },
    {
      icon: FileDigit,
      label: "Receipt no.",
      value: transaction.invoice_number || "—",
    },
    { icon: StickyNote, label: "Notes", value: transaction.notes || "—" },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/transactions">
            <ArrowLeft className="mr-1 h-4 w-4" /> Back
          </Link>
        </Button>
        <h1 className="text-2xl font-bold tracking-tight">
          Transaction details
        </h1>
      </div>

      <Card>
        <CardHeader className="border-b bg-muted/30">
          <CardTitle className="text-lg">{transaction.description}</CardTitle>
        </CardHeader>
        <CardContent className="divide-y p-0">
          {details.map(({ icon: Icon, label, value, highlight }) => (
            <div key={label} className="flex items-center gap-3 px-6 py-3.5">
              <Icon className="h-4 w-4 shrink-0 text-muted-foreground" />
              <dt className="w-28 text-sm text-muted-foreground">{label}</dt>
              <dd
                className={
                  highlight
                    ? "text-lg font-bold tabular-nums text-primary"
                    : "text-sm font-medium"
                }
              >
                {value}
              </dd>
            </div>
          ))}
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-2">
        <Button asChild>
          <Link href={`/invoices/${transaction.id}`}>
            <FileText className="mr-2 h-4 w-4" /> Receipt
          </Link>
        </Button>
        <Button variant="outline" asChild>
          <Link href={`/transactions/${transaction.id}/edit`}>
            <Edit className="mr-2 h-4 w-4" /> Edit
          </Link>
        </Button>
      </div>
    </div>
  )
}
