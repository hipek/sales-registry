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
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <Button asChild>
          <Link href="/transactions/new">
            <Plus className="mr-2 h-4 w-4" /> Dodaj transakcję
          </Link>
        </Button>
      </div>

      {limit.is_exceeded && (
        <div className="p-4 bg-red-100 border border-red-300 rounded-md text-red-800">
          ⚠️ Przekroczyłeś limit kwartalny!
        </div>
      )}

      <LimitGauge
        year={limit.year}
        quarter={limit.quarter}
        limit={limit.limit}
        used={limit.used}
        remaining={limit.remaining}
        isExceeded={limit.is_exceeded}
      />

      <RecentTransactions transactions={transactions} />
    </div>
  )
}
