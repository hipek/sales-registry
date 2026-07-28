"use client"

import { useEffect, useState, use } from "react"
import { api } from "@/lib/api-client"
import { TransactionForm } from "@/components/transactions/transaction-form"

interface TransactionData {
  id: string
  date: string
  description: string
  amount: number
  notes?: string
}

interface EditPageProps {
  params: Promise<{ id: string }>
}

export default function EditTransactionPage({ params }: EditPageProps) {
  const [transaction, setTransaction] = useState<TransactionData | null>(null)
  const [loading, setLoading] = useState(true)
  const [fetchError, setFetchError] = useState<string | null>(null)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const resolvedParams = use(params)

  useEffect(() => {
    api
      .get<TransactionData>(`/api/transactions/${resolvedParams.id}`)
      .then(setTransaction)
      .catch((e) =>
        setFetchError(
          e instanceof Error ? e.message : "Failed to load transaction",
        ),
      )
      .finally(() => setLoading(false))
  }, [resolvedParams.id])

  const handleSubmit = async (data: {
    date: string
    description: string
    amount: number
    notes?: string
  }) => {
    setSubmitError(null)
    try {
      await api.put(`/api/transactions/${resolvedParams.id}`, {
        date: data.date,
        description: data.description,
        amount: data.amount,
        notes: data.notes,
      })
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : "An error occurred")
      throw e // re-throw to prevent navigation
    }
  }

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold">Edit transaction</h1>
        <p className="text-muted-foreground">Loading transaction...</p>
      </div>
    )
  }

  if (fetchError) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold">Edit transaction</h1>
        <div className="p-4 bg-red-100 border border-red-300 rounded-md text-red-800">
          {fetchError}
        </div>
      </div>
    )
  }

  if (!transaction) return null

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Edit transaction</h1>
      {submitError && (
        <div className="p-4 bg-red-100 border border-red-300 rounded-md text-red-800">
          {submitError}
        </div>
      )}
      <TransactionForm
        initialData={transaction}
        onSubmit={handleSubmit}
        submitLabel="Save"
      />
    </div>
  )
}
