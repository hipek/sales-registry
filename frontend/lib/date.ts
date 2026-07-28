import { format, parse } from "date-fns"
import { pl } from "date-fns/locale/pl"

export function formatDate(dateStr: string): string {
  const date = parse(dateStr, "yyyy-MM-dd", new Date())
  return format(date, "d MMMM yyyy", { locale: pl })
}

export function getToday(): string {
  return format(new Date(), "yyyy-MM-dd")
}
