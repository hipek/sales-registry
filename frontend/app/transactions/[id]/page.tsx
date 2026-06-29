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
  params: { id: string }
}) {
  const transaction = await getTransaction(params.id)

  return <TransactionDetail transaction={transaction} />
}
