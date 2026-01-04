from __future__ import annotations

from app.integrations.base import PlatformHTTP


class ShopeeClient:
    """
    NOTE: Endpoint paths/auth here are placeholders.
    Implement per Shopee Open Platform for your region (signed requests, partner_id, shop_id, etc.).
    """
    def __init__(self, *, base_url: str, access_token: str):
        self.http = PlatformHTTP(base_url=base_url)
        self.access_token = access_token

    def list_orders(self, *, time_from: int, time_to: int, cursor: str | None = None, page_size: int = 50) -> dict:
        return self.http.request(
            "GET",
            "/orders/list",
            headers={"Authorization": f"Bearer {self.access_token}"},
            params={"time_from": time_from, "time_to": time_to, "cursor": cursor, "page_size": page_size},
        )

    def get_order_detail(self, *, order_ids: list[str]) -> dict:
        return self.http.request(
            "POST",
            "/orders/detail",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json={"order_ids": order_ids},
        )

    def update_stock(self, *, items: list[dict]) -> dict:
        return self.http.request(
            "POST",
            "/inventory/update",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json={"items": items},
        )
