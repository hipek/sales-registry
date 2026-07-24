"use client"

import { useEffect, useState, use } from "react"
import { api } from "@/lib/api-client"
import { InvoicePreview } from "@/components/invoices/invoice-preview"

interface InvoicePageProps {
  params: Promise<{ id: string }>
}

export default function InvoicePage({ params }: InvoicePageProps) {
  const [invoice, setInvoice] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  const resolvedParams = use(params)

  useEffect(() => {
    api.get(`/api/invoices/${resolvedParams.id}`).then((data) => {
      setInvoice(data)
      setLoading(false)
    })
  }, [resolvedParams.id])

  if (loading) return <div className="p-8">Loading...</div>
  if (!invoice) return <div className="p-8">Invoice not found</div>

  return <InvoicePreview invoice={invoice} transactionId={resolvedParams.id} />
}
