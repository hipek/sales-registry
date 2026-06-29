"use client"

import { api } from "@/lib/api-client"
import { TransactionForm } from "@/components/transactions/transaction-form"

export default function NewTransactionPage() {
  const handleSubmit = async (data: { date: string; description: string; amount: number; notes?: string }) => {
    await api.post("/api/transactions", {
      date: data.date,
      description: data.description,
      amount: data.amount,
      notes: data.notes,
    })
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Dodaj transakcję</h1>
      <TransactionForm onSubmit={handleSubmit} submitLabel="Dodaj" />
    </div>
  )
}
