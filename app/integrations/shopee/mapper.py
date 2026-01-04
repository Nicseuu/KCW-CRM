from __future__ import annotations

def map_status(shopee_status: str | None) -> str:
    s = (shopee_status or "").upper().strip()
    return {
        "UNPAID": "PENDING",
        "READY_TO_SHIP": "CONFIRMED",   # treated as paid/confirmed
        "PROCESSED": "PACKING",
        "SHIPPED": "SHIPPED",
        "COMPLETED": "DELIVERED",
        "CANCELLED": "CANCELLED",
        "REFUNDED": "REFUNDED",
        "RETURNED": "RETURNED",
    }.get(s, "PENDING")
