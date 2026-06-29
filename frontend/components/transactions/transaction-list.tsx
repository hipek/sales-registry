import Link from "next/link"
import { formatPLN } from "@/lib/format"
import { formatDate } from "@/lib/date"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Plus, Download, Trash2 } from "lucide-react"

interface Transaction {
  id: string
  date: string
  description: string
  amount: number
  invoice_number?: string
}

interface PaginationMeta {
  page: number
  limit: number
  total: number
  total_pages: number
}

interface TransactionListProps {
  transactions: Transaction[]
  meta: PaginationMeta
  search: string
  from_date: string
  to_date: string
  onSearch: (val: string) => void
  onDateFilter: (from: string, to: string) => void
  onDelete: (id: string) => void
}

export function TransactionList({
  transactions,
  meta,
  search,
  onSearch,
  onDelete,
}: TransactionListProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Transakcje</h1>
        <div className="flex gap-2">
          <Button variant="outline" asChild>
            <a href="/api/transactions/export">
              <Download className="mr-2 h-4 w-4" /> Eksport CSV
            </a>
          </Button>
          <Button asChild>
            <Link href="/transactions/new">
              <Plus className="mr-2 h-4 w-4" /> Dodaj
            </Link>
          </Button>
        </div>
      </div>

      <div className="flex gap-2">
        <Input
          placeholder="Szukaj opisu..."
          value={search}
          onChange={(e) => onSearch(e.target.value)}
          className="max-w-xs"
        />
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Data</TableHead>
            <TableHead>Opis</TableHead>
            <TableHead>Kwota</TableHead>
            <TableHead>Paragon</TableHead>
            <TableHead className="w-20">Akcje</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {transactions.length === 0 ? (
            <TableRow>
              <TableCell colSpan={5} className="text-center text-muted-foreground">
                Brak transakcji
              </TableCell>
            </TableRow>
          ) : (
            transactions.map((t) => (
              <TableRow key={t.id}>
                <TableCell>{formatDate(t.date)}</TableCell>
                <TableCell>
                  <Link href={`/transactions/${t.id}`} className="hover:underline">
                    {t.description}
                  </Link>
                </TableCell>
                <TableCell className="font-medium">{formatPLN(t.amount)}</TableCell>
                <TableCell>{t.invoice_number || "—"}</TableCell>
                <TableCell>
                  <div className="flex gap-1">
                    <Button variant="ghost" size="icon" asChild>
                      <Link href={`/transactions/${t.id}`}>👁</Link>
                    </Button>
                    <Button variant="ghost" size="icon" asChild>
                      <Link href={`/transactions/${t.id}/edit`}>✏️</Link>
                    </Button>
                    <Button variant="ghost" size="icon" onClick={() => onDelete(t.id)}>
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>

      {meta.total_pages > 1 && (
        <div className="flex justify-center gap-2">
          {Array.from({ length: meta.total_pages }, (_, i) => (
            <Button
              key={i + 1}
              variant={meta.page === i + 1 ? "default" : "outline"}
              size="sm"
              asChild
            >
              <Link href={`/transactions?page=${i + 1}`}>{i + 1}</Link>
            </Button>
          ))}
        </div>
      )}
    </div>
  )
}
