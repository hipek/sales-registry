"use client"

import { api } from "@/lib/api-client"
import { TransactionForm } from "@/components/transactions/transaction-form"

interface EditPageProps {
  params: { id: string }
}

export default function EditTransactionPage({ params }: EditPageProps) {
  const handleSubmit = async (data: { date: string; description: string; amount: number; notes?: string }) => {
    await api.put(`/api/transactions/${params.id}`, {
      date: data.date,
      description: data.description,
      amount: data.amount,
      notes: data.notes,
    })
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Edytuj transakcję</h1>
      <TransactionForm onSubmit={handleSubmit} submitLabel="Zapisz" />
    </div>
  )
}
