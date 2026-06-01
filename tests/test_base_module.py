from unittest.mock import AsyncMock

import pytest

from kai_sdk_python.modules.base_module import BaseModule
from kai_sdk_python.modules.http_client import RetryOptions


class ConcreteModule(BaseModule):
    pass


async def test_post_delegates_to_http_client():
    module = ConcreteModule({"api-key": "k"}, "https://api.example.com/")
    module._http.post = AsyncMock(return_value={"result": True})

    result = await module._post("api/test", {"a": 1})

    module._http.post.assert_called_once_with("api/test", {"a": 1})
    assert result == {"result": True}


async def test_download_delegates_to_http_client():
    module = ConcreteModule({"api-key": "k"}, "https://api.example.com/")
    module._http.download = AsyncMock(return_value=b"bytes")

    result = await module._download("api/download", {"id": "x"})

    module._http.download.assert_called_once_with("api/download", {"id": "x"})
    assert result == b"bytes"


async def test_accepts_retry_options():
    opts = RetryOptions(max_retries=5, retry_delay=0.5, timeout=60.0)
    module = ConcreteModule({"api-key": "k"}, "https://api.example.com/", opts)
    assert module._http._max_retries == 5
    assert module._http._retry_delay == 0.5
    assert module._http._timeout == 60.0
