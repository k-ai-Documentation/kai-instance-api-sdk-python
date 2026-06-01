from typing import Any

from .http_client import HttpClient, RetryOptions


class BaseModule:
    def __init__(self, headers: dict, base_url: str, retry_options: RetryOptions | None = None):
        self._http = HttpClient(headers, base_url, retry_options)

    async def _post(self, endpoint: str, data: dict | None = None) -> Any:
        return await self._http.post(endpoint, data)

    async def _download(self, endpoint: str, data: dict | None = None) -> bytes:
        return await self._http.download(endpoint, data)
