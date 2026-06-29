import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface LimitGaugeProps {
  year: number
  quarter: number
  limit: number
  used: number
  remaining: number
  isExceeded: boolean
}

export function LimitGauge({ year, quarter, limit, used, remaining, isExceeded }: LimitGaugeProps) {
  const percentage = limit > 0 ? (used / limit) * 100 : 0
  const barColor = isExceeded ? "bg-red-500" : percentage > 80 ? "bg-yellow-500" : "bg-green-500"

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0">
        <CardTitle>Limit kwartalny {year} (Q{quarter})</CardTitle>
        <Badge variant={isExceeded ? "destructive" : "default"}>
          {isExceeded ? "Przekroczony" : "OK"}
        </Badge>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="h-4 w-full rounded-full bg-muted">
            <div
              className={`h-4 rounded-full ${barColor} transition-all`}
              style={{ width: `${Math.min(percentage, 100)}%` }}
            />
          </div>
          <div className="flex justify-between text-sm">
            <span>Wykorzystane: {used.toFixed(2)} PLN</span>
            <span>Pozostało: {remaining.toFixed(2)} PLN</span>
          </div>
          <div className="text-sm text-muted-foreground">
            Limit: {limit.toFixed(2)} PLN
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
