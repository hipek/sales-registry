"use client"

import { useEffect, useState, useCallback } from "react"
import { api } from "@/lib/api-client"
import { TransactionList } from "@/components/transactions/transaction-list"

export default function TransactionsPage() {
  const [data, setData] = useState<{ data: any[]; meta: any } | null>(null)
  const [search, setSearch] = useState("")
  const [fromDate, setFromDate] = useState("")
  const [toDate, setToDate] = useState("")
  const [loading, setLoading] = useState(true)

  const fetchData = useCallback(async () => {
    setLoading(true)
    const params = new URLSearchParams()
    if (search) params.set("search", search)
    if (fromDate) params.set("from_date", fromDate)
    if (toDate) params.set("to_date", toDate)
    const result = await api.get<{ data: any[]; meta: any }>(`/api/transactions?${params.toString()}`)
    setData(result)
    setLoading(false)
  }, [search, fromDate, toDate])

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
      fromDate={fromDate}
      toDate={toDate}
      onSearch={(val) => setSearch(val)}
      onDateFilter={(from, to) => { setFromDate(from); setToDate(to) }}
      onDelete={handleDelete}
    />
  )
}
