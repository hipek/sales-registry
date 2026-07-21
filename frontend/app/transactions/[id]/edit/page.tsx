"use client"

import { useState } from "react"
import { api } from "@/lib/api-client"
import { TransactionForm } from "@/components/transactions/transaction-form"

interface EditPageProps {
  params: { id: string }
}

export default function EditTransactionPage({ params }: EditPageProps) {
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (data: { date: string; description: string; amount: number; notes?: string }) => {
    setError(null)
    try {
      await api.put(`/api/transactions/${params.id}`, {
        date: data.date,
        description: data.description,
        amount: data.amount,
        notes: data.notes,
      })
    } catch (e) {
      setError(e instanceof Error ? e.message : "Wystąpił błąd")
      throw e // re-throw to prevent navigation
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Edytuj transakcję</h1>
      {error && (
        <div className="p-4 bg-red-100 border border-red-300 rounded-md text-red-800">
          {error}
        </div>
      )}
      <TransactionForm onSubmit={handleSubmit} submitLabel="Zapisz" />
    </div>
  )
}
