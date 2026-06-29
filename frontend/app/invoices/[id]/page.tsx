"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api-client"
import { InvoicePreview } from "@/components/invoices/invoice-preview"

interface InvoicePageProps {
  params: { id: string }
}

export default function InvoicePage({ params }: InvoicePageProps) {
  const [invoice, setInvoice] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get(`/api/invoices/${params.id}`).then((data) => {
      setInvoice(data)
      setLoading(false)
    })
  }, [params.id])

  if (loading) return <div className="p-8">Ładowanie...</div>
  if (!invoice) return <div className="p-8">Nie znaleziono faktury</div>

  return <InvoicePreview invoice={invoice} transactionId={params.id} />
}
