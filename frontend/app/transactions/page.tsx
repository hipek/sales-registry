"use client"

import { useEffect, useState, useCallback } from "react"
import { api } from "@/lib/api-client"
import { TransactionList } from "@/components/transactions/transaction-list"

export default function TransactionsPage() {
  const [data, setData] = useState<{ data: any[]; meta: any } | null>(null)
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(true)

  const fetchData = useCallback(async () => {
    setLoading(true)
    const params = new URLSearchParams()
    if (search) params.set("search", search)
    const result = await api.get<{ data: any[]; meta: any }>(`/api/transactions?${params.toString()}`)
    setData(result)
    setLoading(false)
  }, [search])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  const handleDelete = async (id: string) => {
    if (!confirm("Czy na pewno chcesz usunąć tę transakcję?")) return
    await api.delete(`/api/transactions/${id}`)
    fetchData()
  }

  if (loading && !data) return <div className="p-8">Ładowanie...</div>

  return (
    <TransactionList
      transactions={data?.data || []}
      meta={data?.meta || { page: 1, limit: 10, total: 0, total_pages: 1 }}
      search={search}
      from_date=""
      to_date=""
      onSearch={(val) => setSearch(val)}
      onDateFilter={() => {}}
      onDelete={handleDelete}
    />
  )
}
