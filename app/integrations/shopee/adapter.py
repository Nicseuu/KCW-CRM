from __future__ import annotations

from app.integrations.base import with_retries
from app.integrations.shopee.client import ShopeeClient


class ShopeeAdapter:
    def __init__(self, *, base_url: str, access_token: str):
        self.client = ShopeeClient(base_url=base_url, access_token=access_token)

    def pull_orders(self, *, time_from: int, time_to: int) -> dict:
        return with_retries(lambda: self.client.list_orders(time_from=time_from, time_to=time_to))

    def pull_order_details(self, *, order_ids: list[str]) -> dict:
        return with_retries(lambda: self.client.get_order_detail(order_ids=order_ids))

    def push_stock(self, *, items: list[dict]) -> dict:
        return with_retries(lambda: self.client.update_stock(items=items))
