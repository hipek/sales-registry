import { api } from "@/lib/api-client"
import { TransactionDetail } from "@/components/transactions/transaction-detail"

export const dynamic = "force-dynamic"

interface TransactionData {
  id: string
  date: string
  description: string
  amount: number
  invoice_number?: string
  notes?: string
}

async function getTransaction(id: string) {
  return api.get<TransactionData>(`/api/transactions/${id}`)
}

export default async function TransactionDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const transaction = await getTransaction(id)

  return <TransactionDetail transaction={transaction} />
}
