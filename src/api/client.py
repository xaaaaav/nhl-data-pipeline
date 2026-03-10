import asyncio
import time
from types import TracebackType
from typing import Any

import httpx
import structlog
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

logger = structlog.get_logger(__name__)

WEB_BASE = "https://api-web.nhle.com/v1"
STATS_BASE = "https://api.nhle.com/stats/rest/en"
SEARCH_BASE = "https://search.d3.nhle.com/api/v1"


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in (429, 500, 502, 503, 504)
    return isinstance(exc, (httpx.TimeoutException, httpx.ConnectError))


class _TokenBucket:
    """Simple token bucket rate limiter."""

    def __init__(self, rate: float) -> None:
        self._rate = rate  # tokens per second
        self._tokens: float = rate
        self._last: float = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last
            self._last = now
            self._tokens = min(self._rate, self._tokens + elapsed * self._rate)
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return
            wait_time = (1.0 - self._tokens) / self._rate
            self._tokens = 0.0
        await asyncio.sleep(wait_time)


class NHLApiClient:
    WEB_BASE = WEB_BASE
    STATS_BASE = STATS_BASE
    SEARCH_BASE = SEARCH_BASE

    def __init__(self, requests_per_second: float = 2.0) -> None:
        self._rate = requests_per_second
        self._bucket = _TokenBucket(requests_per_second)
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                follow_redirects=True,
            )
        return self._client

    async def get(
        self, base: str, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        url = f"{base}{path}"
        await self._bucket.acquire()
        return await self._get_with_retry(url, params)

    @retry(
        retry=retry_if_exception(_is_retryable),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _get_with_retry(
        self, url: str, params: dict[str, Any] | None
    ) -> dict[str, Any]:
        client = await self._get_client()
        log = logger.bind(url=url, params=params)
        log.debug("http.get")
        response = await client.get(url, params=params)
        response.raise_for_status()
        log.debug("http.ok", status=response.status_code)
        result: dict[str, Any] = response.json()
        return result

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def __aenter__(self) -> "NHLApiClient":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()
