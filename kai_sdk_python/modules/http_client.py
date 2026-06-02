import asyncio
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class RetryOptions:
    """Configuration for HTTP retry behaviour.

    Attributes:
        max_retries: Number of additional attempts after the first failure (default 3).
        retry_delay: Base delay in seconds between retries; doubles on each attempt (default 1.0).
        timeout: Per-request timeout in seconds (default 30.0).
    """

    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 30.0


class HttpClient:
    """Low-level async HTTP client with exponential-backoff retry for transient errors."""

    RETRYABLE_STATUSES = {502, 503, 504}

    def __init__(self, headers: dict, base_url: str, retry_options: RetryOptions | None = None):
        """Initialise the client.

        Args:
            headers: Request headers sent with every call (e.g. ``api-key``, ``instance-id``).
            base_url: Base URL prepended to all endpoint paths.
            retry_options: Retry and timeout settings. Falls back to :class:`RetryOptions` defaults.
        """
        self._headers = headers
        self._base_url = base_url
        opts = retry_options or RetryOptions()
        self._max_retries = opts.max_retries
        self._retry_delay = opts.retry_delay
        self._timeout = opts.timeout

    async def post(self, endpoint: str, data: dict | None = None) -> Any:
        """POST JSON to *endpoint* and return the unwrapped ``response`` field.

        Retries on HTTP 502/503/504 and network errors with exponential backoff.

        Args:
            endpoint: Path relative to the base URL.
            data: JSON-serialisable payload. ``None`` sends an empty body.

        Returns:
            The value of ``response.json()["response"]``.

        Raises:
            httpx.HTTPStatusError: For non-retryable HTTP errors (4xx, 500).
            httpx.RequestError: If all retry attempts exhaust on network errors.
        """
        return await self._with_retry(self._do_post, endpoint, data)

    async def download(self, endpoint: str, data: dict | None = None) -> bytes:
        """POST JSON to *endpoint* and return the raw response bytes.

        Retries on HTTP 502/503/504 and network errors with exponential backoff.

        Args:
            endpoint: Path relative to the base URL.
            data: JSON-serialisable payload. ``None`` sends an empty body.

        Returns:
            Raw response content as ``bytes``.

        Raises:
            httpx.HTTPStatusError: For non-retryable HTTP errors.
            httpx.RequestError: If all retry attempts exhaust on network errors.
        """
        return await self._with_retry(self._do_download, endpoint, data)

    async def _do_post(self, endpoint: str, data: dict | None) -> Any:
        async with httpx.AsyncClient(
            headers=self._headers,
            base_url=self._base_url,
            verify=False,
            timeout=self._timeout,
        ) as client:
            response = await client.post(endpoint, json=data)
            response.raise_for_status()
            return response.json()["response"]

    async def _do_download(self, endpoint: str, data: dict | None) -> bytes:
        async with httpx.AsyncClient(
            headers=self._headers,
            base_url=self._base_url,
            verify=False,
            timeout=self._timeout,
        ) as client:
            response = await client.post(endpoint, json=data)
            response.raise_for_status()
            return response.content

    async def _with_retry(self, fn, *args) -> Any:
        """Execute *fn* with exponential-backoff retry on retryable errors.

        Backoff formula: ``retry_delay * 2^attempt``. Non-retryable status codes
        (4xx, 500) are re-raised immediately without further attempts.
        """
        last_error: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                return await fn(*args)
            except httpx.RequestError as e:
                last_error = e
                if attempt < self._max_retries:
                    await asyncio.sleep(self._retry_delay * (2 ** attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code in self.RETRYABLE_STATUSES:
                    last_error = e
                    if attempt < self._max_retries:
                        await asyncio.sleep(self._retry_delay * (2 ** attempt))
                else:
                    raise
        assert last_error is not None
        raise last_error
