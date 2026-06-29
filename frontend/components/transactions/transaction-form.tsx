"use client"

import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { getToday } from "@/lib/date"

interface FormData {
  date: string
  description: string
  amount: string
  notes?: string
}

interface TransactionFormProps {
  initialData?: {
    date: string
    description: string
    amount: number
    notes?: string
  }
  onSubmit: (data: { date: string; description: string; amount: number; notes?: string }) => Promise<void>
  submitLabel: string
}

export function TransactionForm({ initialData, onSubmit, submitLabel }: TransactionFormProps) {
  const router = useRouter()
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    defaultValues: initialData ? {
      date: initialData.date,
      description: initialData.description,
      amount: String(initialData.amount),
      notes: initialData.notes || "",
    } : {
      date: getToday(),
      description: "",
      amount: "",
      notes: "",
    },
  })

  const onFormSubmit = async (data: FormData) => {
    const amount = parseFloat(data.amount)
    if (isNaN(amount) || amount <= 0) return
    await onSubmit({
      date: data.date,
      description: data.description,
      amount,
      notes: data.notes,
    })
    router.push("/transactions")
  }

  return (
    <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-4">
      <div>
        <Label htmlFor="date">Data</Label>
        <Input id="date" type="date" {...register("date", { required: "Data jest wymagana" })} />
        {errors.date && <p className="text-sm text-destructive">{errors.date.message}</p>}
      </div>

      <div>
        <Label htmlFor="description">Opis</Label>
        <Input id="description" {...register("description", {
          required: "Opis jest wymagany",
          maxLength: { value: 500, message: "Opis nie może mieć więcej niż 500 znaków" },
        })} />
        {errors.description && <p className="text-sm text-destructive">{errors.description.message}</p>}
      </div>

      <div>
        <Label htmlFor="amount">Kwota (PLN)</Label>
        <Input id="amount" type="number" step="0.01" {...register("amount", {
          required: "Kwota jest wymagana",
          validate: (value) => parseFloat(value) > 0 || "Kwota musi być większa od 0",
        })} />
        {errors.amount && <p className="text-sm text-destructive">{errors.amount.message}</p>}
      </div>

      <div>
        <Label htmlFor="notes">Notatki (opcjonalne)</Label>
        <Input id="notes" {...register("notes")} />
      </div>

      <div className="flex gap-2">
        <Button type="submit">{submitLabel}</Button>
        <Button type="button" variant="outline" onClick={() => router.back()}>
          Anuluj
        </Button>
      </div>
    </form>
  )
}
