from typing import Any

from .http_client import HttpClient, RetryOptions


class BaseModule:
    """Abstract base class shared by all SDK modules.

    Wraps :class:`~kai_sdk_python.modules.http_client.HttpClient` and exposes
    ``_post`` / ``_download`` helpers so subclasses don't interact with the HTTP
    layer directly.
    """

    def __init__(self, headers: dict, base_url: str, retry_options: RetryOptions | None = None):
        """Initialise the module with shared HTTP infrastructure.

        Args:
            headers: Authentication headers forwarded to every request.
            base_url: Base URL for the target KAI Studio instance.
            retry_options: Optional retry/timeout settings.
        """
        self._http = HttpClient(headers, base_url, retry_options)

    async def _post(self, endpoint: str, data: dict | None = None) -> Any:
        """Send a POST request and return the unwrapped JSON response.

        Args:
            endpoint: Path relative to the base URL.
            data: Request payload to JSON-serialise.
        """
        return await self._http.post(endpoint, data)

    async def _download(self, endpoint: str, data: dict | None = None) -> bytes:
        """Send a POST request and return raw response bytes.

        Args:
            endpoint: Path relative to the base URL.
            data: Request payload to JSON-serialise.
        """
        return await self._http.download(endpoint, data)
