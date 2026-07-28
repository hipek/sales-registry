import Link from "next/link"
import { LimitGauge } from "./limit-gauge"
import { RecentTransactions } from "./recent-transactions"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"

interface DashboardProps {
  limit: {
    year: number
    quarter: number
    limit: number
    used: number
    remaining: number
    is_exceeded: boolean
  }
  transactions: Array<{
    id: string
    date: string
    description: string
    amount: number
  }>
}

export function Dashboard({ limit, transactions }: DashboardProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Sales summary for non-registered business
          </p>
        </div>
        <Button asChild>
          <Link href="/transactions/new">
            <Plus className="mr-2 h-4 w-4" /> Add transaction
          </Link>
        </Button>
      </div>

      {limit.is_exceeded && (
        <div className="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-200">
          <span className="font-semibold">⚠️ Quarterly limit exceeded!</span>{" "}
          Reached {limit.used.toFixed(2)} PLN of {limit.limit.toFixed(2)} PLN.
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-5">
        <div className="lg:col-span-3">
          <LimitGauge
            year={limit.year}
            quarter={limit.quarter}
            limit={limit.limit}
            used={limit.used}
            remaining={limit.remaining}
            isExceeded={limit.is_exceeded}
          />
        </div>
        <div className="lg:col-span-2">
          <RecentTransactions transactions={transactions} />
        </div>
      </div>
    </div>
  )
}
