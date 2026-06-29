import { api } from "@/lib/api-client"
import { Dashboard } from "@/components/dashboard"

export const dynamic = "force-dynamic"

interface LimitData {
  year: number
  quarter: number
  limit: number
  used: number
  remaining: number
  is_exceeded: boolean
}

interface TransactionData {
  id: string
  date: string
  description: string
  amount: number
}

async function getDashboardData() {
  const [limit, transactions] = await Promise.all([
    api.get<LimitData>("/api/limits/current"),
    api.get<{ data: TransactionData[] }>("/api/transactions?limit=10"),
  ])
  return { limit, transactions: transactions.data }
}

export default async function HomePage() {
  const { limit, transactions } = await getDashboardData()

  return <Dashboard limit={limit} transactions={transactions} />
}
