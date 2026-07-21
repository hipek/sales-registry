import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AlertTriangle, CheckCircle2, TrendingUp } from "lucide-react"
import { cn } from "@/lib/utils"

interface LimitGaugeProps {
  year: number
  quarter: number
  limit: number
  used: number
  remaining: number
  isExceeded: boolean
}

export function LimitGauge({ year, quarter, limit, used, remaining, isExceeded }: LimitGaugeProps) {
  const percentage = limit > 0 ? Math.min((used / limit) * 100, 100) : 0

  const barColor = isExceeded
    ? "from-red-500 to-red-400"
    : percentage > 80
    ? "from-amber-500 to-yellow-400"
    : "from-emerald-500 to-green-400"

  const statusIcon = isExceeded
    ? <AlertTriangle className="h-4 w-4" />
    : <CheckCircle2 className="h-4 w-4" />

  const statusLabel = isExceeded ? "Exceeded" : percentage > 80 ? "Near limit" : "Normal"
  const statusVariant = isExceeded ? "destructive" : percentage > 80 ? "secondary" : "default"

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
        <div>
          <CardTitle className="text-base">Quarterly limit</CardTitle>
          <p className="text-xs text-muted-foreground mt-0.5">Q{quarter} {year}</p>
        </div>
        <Badge variant={statusVariant} className="gap-1 font-normal">
          {statusIcon}
          {statusLabel}
        </Badge>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Usage</span>
            <span className="font-semibold tabular-nums">{percentage.toFixed(1)}%</span>
          </div>
          <div className="relative h-3 w-full overflow-hidden rounded-full bg-muted">
            <div
              className={cn("h-full w-full rounded-full bg-gradient-to-r transition-all duration-500", barColor)}
              style={{ width: `${percentage}%` }}
            />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 rounded-lg bg-muted/50 p-3">
          <div>
            <dt className="text-xs text-muted-foreground">Used</dt>
            <dd className={cn(
              "mt-0.5 text-sm font-semibold tabular-nums",
              isExceeded && "text-destructive"
            )}>
              {used.toFixed(2)} PLN
            </dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">Remaining</dt>
            <dd className="mt-0.5 text-sm font-semibold tabular-nums text-emerald-600">
              {remaining.toFixed(2)} PLN
            </dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">Limit</dt>
            <dd className="mt-0.5 text-sm font-semibold tabular-nums">
              {limit.toFixed(2)} PLN
            </dd>
          </div>
        </div>

        {!isExceeded && percentage > 0 && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <TrendingUp className="h-3.5 w-3.5 text-primary" />
            <span>
              Used {used.toFixed(2)} PLN of {limit.toFixed(2)} PLN quarterly limit
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
