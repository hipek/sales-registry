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
import { Plus, Download, Trash2, Eye, Pencil, Search, Calendar } from "lucide-react"

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
  fromDate: string
  toDate: string
  onSearch: (val: string) => void
  onDateFilter: (from: string, to: string) => void
  onDelete: (id: string) => void
}

export function TransactionList({
  transactions,
  meta,
  search,
  fromDate,
  toDate,
  onSearch,
  onDateFilter,
  onDelete,
}: TransactionListProps) {
  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Transakcje</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            {meta.total} {meta.total === 1 ? "transakcja" : meta.total % 10 >= 2 && meta.total % 10 <= 4 && meta.total % 100 / 10 >= 2 ? "transakcje" : "transakcji"}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" asChild>
            <a href="/api/transactions/export">
              <Download className="mr-2 h-4 w-4" /> CSV
            </a>
          </Button>
          <Button size="sm" asChild>
            <Link href="/transactions/new">
              <Plus className="mr-2 h-4 w-4" /> Dodaj
            </Link>
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Szukaj opisu..."
            value={search}
            onChange={(e) => onSearch(e.target.value)}
            className="pl-8 max-w-xs"
          />
        </div>
        <div className="flex items-center gap-2">
          <Calendar className="h-4 w-4 text-muted-foreground shrink-0" />
          <Input
            type="date"
            value={fromDate}
            onChange={(e) => onDateFilter(e.target.value, toDate)}
            className="w-40"
            title="Od daty"
          />
          <span className="text-xs text-muted-foreground">–</span>
          <Input
            type="date"
            value={toDate}
            onChange={(e) => onDateFilter(fromDate, e.target.value)}
            className="w-40"
            title="Do daty"
          />
        </div>
      </div>

      <div className="rounded-lg border bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Data</TableHead>
              <TableHead>Opis</TableHead>
              <TableHead className="text-right">Kwota</TableHead>
              <TableHead>Paragon</TableHead>
              <TableHead className="w-24 text-right">Akcje</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {transactions.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="h-32 text-center">
                  <p className="text-sm text-muted-foreground">Brak transakcji</p>
                  <Button variant="link" size="sm" asChild>
                    <Link href="/transactions/new">Dodaj pierwszą transakcję</Link>
                  </Button>
                </TableCell>
              </TableRow>
            ) : (
              transactions.map((t) => (
                <TableRow key={t.id} className="group">
                  <TableCell className="tabular-nums text-muted-foreground">
                    {formatDate(t.date)}
                  </TableCell>
                  <TableCell>
                    <Link href={`/transactions/${t.id}`} className="font-medium hover:text-primary hover:underline">
                      {t.description}
                    </Link>
                  </TableCell>
                  <TableCell className="text-right font-semibold tabular-nums">
                    {formatPLN(t.amount)}
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {t.invoice_number || "—"}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-0.5 opacity-60 transition-opacity group-hover:opacity-100">
                      <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
                        <Link href={`/transactions/${t.id}`}>
                          <Eye className="h-3.5 w-3.5" />
                          <span className="sr-only">Szczegóły</span>
                        </Link>
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
                        <Link href={`/transactions/${t.id}/edit`}>
                          <Pencil className="h-3.5 w-3.5" />
                          <span className="sr-only">Edytuj</span>
                        </Link>
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-destructive/10" onClick={() => onDelete(t.id)}>
                        <Trash2 className="h-3.5 w-3.5 text-destructive" />
                        <span className="sr-only">Usuń</span>
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {meta.total_pages > 1 && (
        <div className="flex items-center justify-center gap-1">
          {Array.from({ length: meta.total_pages }, (_, i) => (
            <Button
              key={i + 1}
              variant={meta.page === i + 1 ? "default" : "outline"}
              size="sm"
              className="min-w-[2rem]"
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
