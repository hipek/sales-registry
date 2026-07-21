import calendar
from datetime import date


def get_current_quarter() -> tuple[int, int]:
    """Return (year, quarter) for the current date."""
    today = date.today()
    quarter = (today.month - 1) // 3 + 1
    return today.year, quarter


def get_quarter_date_range(year: int, quarter: int) -> tuple[date, date]:
    """Return (start_date, end_date) for a given year/quarter."""
    start_month = (quarter - 1) * 3 + 1
    end_month = start_month + 2
    _, last_day = calendar.monthrange(year, end_month)
    return date(year, start_month, 1), date(year, end_month, last_day)
