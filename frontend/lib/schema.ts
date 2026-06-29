import { sqliteTable, text, real, integer } from "drizzle-orm/sqlite-core"

export const transactions = sqliteTable("transactions", {
  id: text("id").primaryKey(),
  date: text("date").notNull(),
  description: text("description").notNull(),
  amount: real("amount").notNull(),
  invoice_number: text("invoice_number"),
  notes: text("notes"),
  deleted_at: text("deleted_at"),
  created_at: text("created_at").notNull(),
  updated_at: text("updated_at").notNull(),
})

export const counters = sqliteTable("counters", {
  id: text("id").primaryKey(),
  value: integer("value").notNull().default(0),
})
