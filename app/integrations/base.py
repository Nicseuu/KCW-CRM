from __future__ import annotations

import time
import httpx


class RateLimitError(Exception):
    pass


class PlatformHTTP:
    def __init__(self, base_url: str, timeout_s: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=timeout_s)

    def request(self, method: str, path: str, *, headers: dict | None = None, params: dict | None = None, json: dict | None = None) -> dict:
        url = f"{self.base_url}{path}"
        resp = self.client.request(method, url, headers=headers, params=params, json=json)

        if resp.status_code in (429, 503):
            raise RateLimitError(f"rate limited: {resp.status_code} {resp.text}")

        resp.raise_for_status()
        return resp.json()


def with_retries(fn, *, max_attempts: int = 5, base_sleep_s: float = 2.0):
    attempt = 1
    while True:
        try:
            return fn()
        except RateLimitError:
            if attempt >= max_attempts:
                raise
            time.sleep(base_sleep_s * (2 ** (attempt - 1)))
            attempt += 1
