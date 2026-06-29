import Link from "next/link"
import { formatPLN } from "@/lib/format"
import { formatDate } from "@/lib/date"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface Transaction {
  id: string
  date: string
  description: string
  amount: number
}

interface RecentTransactionsProps {
  transactions: Transaction[]
}

export function RecentTransactions({ transactions }: RecentTransactionsProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0">
        <CardTitle>Ostatnie transakcje</CardTitle>
        <Button variant="link" asChild>
          <Link href="/transactions">Zobacz wszystkie</Link>
        </Button>
      </CardHeader>
      <CardContent>
        {transactions.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak transakcji</p>
        ) : (
          <ul className="space-y-2">
            {transactions.map((t) => (
              <li key={t.id} className="flex items-center justify-between py-2 border-b">
                <div>
                  <Link href={`/transactions/${t.id}`} className="font-medium hover:underline">
                    {t.description}
                  </Link>
                  <div className="text-xs text-muted-foreground">{formatDate(t.date)}</div>
                </div>
                <span className="font-medium">{formatPLN(t.amount)}</span>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}
