import { z } from "zod"

export const transactionSchema = z.object({
  date: z.string().min(1, "Date is required"),
  description: z.string().min(1, "Description is required").max(500, "Description cannot exceed 500 characters"),
  amount: z.string().transform((val) => parseFloat(val)).pipe(
    z.number().min(0.01, "Amount must be greater than 0")
  ),
  notes: z.string().optional(),
})

export type TransactionInput = z.infer<typeof transactionSchema>
