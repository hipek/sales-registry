from decimal import Decimal
from typing import Any

from pydantic import field_serializer


class DecimalMoneyMixin:
    @field_serializer("*", check_fields=False)
    def serialize_decimal_money(self, value: Any) -> Any:
        if isinstance(value, Decimal):
            return float(value)
        return value