import { z } from "zod"

export const transactionSchema = z.object({
  date: z.string().min(1, "Data jest wymagana"),
  description: z.string().min(1, "Opis jest wymagany").max(500, "Opis nie może mieć więcej niż 500 znaków"),
  amount: z.string().transform((val) => parseFloat(val)).pipe(
    z.number().min(0.01, "Kwota musi być większa od 0")
  ),
  notes: z.string().optional(),
})

export type TransactionInput = z.infer<typeof transactionSchema>
