import Link from "next/link"
import { formatPLN } from "@/lib/format"
import { formatDate } from "@/lib/date"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowRight, Receipt } from "lucide-react"

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
    <Card className="h-full">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
        <CardTitle className="text-base">Recent transactions</CardTitle>
        <Button variant="ghost" size="sm" className="gap-1 text-xs" asChild>
          <Link href="/transactions">
            All <ArrowRight className="h-3 w-3" />
          </Link>
        </Button>
      </CardHeader>
      <CardContent>
        {transactions.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <Receipt className="h-10 w-10 text-muted-foreground/40" />
            <p className="mt-2 text-sm text-muted-foreground">
              No transactions
            </p>
            <Button variant="outline" size="sm" className="mt-3" asChild>
              <Link href="/transactions/new">Add first</Link>
            </Button>
          </div>
        ) : (
          <ul className="space-y-1">
            {transactions.map((t) => (
              <li key={t.id}>
                <Link
                  href={`/transactions/${t.id}`}
                  className="flex items-center justify-between rounded-md px-2 py-2 transition-colors hover:bg-muted/50"
                >
                  <div className="min-w-0">
                    <div className="truncate text-sm font-medium">
                      {t.description}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {formatDate(t.date)}
                    </div>
                  </div>
                  <span className="ml-3 shrink-0 text-sm font-semibold tabular-nums">
                    {formatPLN(t.amount)}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}
