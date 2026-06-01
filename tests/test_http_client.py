from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from kai_sdk_python.modules.http_client import HttpClient, RetryOptions


def make_client(max_retries=3, retry_delay=0.0, timeout=30.0):
    opts = RetryOptions(max_retries=max_retries, retry_delay=retry_delay, timeout=timeout)
    return HttpClient({"api-key": "test"}, "https://api.example.com/", opts)


# --- _with_retry ---

async def test_with_retry_returns_on_success():
    client = make_client()
    async def fn():
        return "ok"
    result = await client._with_retry(fn)
    assert result == "ok"


async def test_with_retry_retries_on_502():
    client = make_client(max_retries=2, retry_delay=0.0)
    calls = 0

    async def fn():
        nonlocal calls
        calls += 1
        resp = MagicMock(status_code=502)
        if calls < 3:
            raise httpx.HTTPStatusError("502", request=MagicMock(), response=resp)
        return "ok"

    with patch("asyncio.sleep", AsyncMock()):
        result = await client._with_retry(fn)

    assert result == "ok"
    assert calls == 3


async def test_with_retry_retries_on_503():
    client = make_client(max_retries=1, retry_delay=0.0)
    calls = 0

    async def fn():
        nonlocal calls
        calls += 1
        resp = MagicMock(status_code=503)
        if calls < 2:
            raise httpx.HTTPStatusError("503", request=MagicMock(), response=resp)
        return "ok"

    with patch("asyncio.sleep", AsyncMock()):
        result = await client._with_retry(fn)

    assert result == "ok"
    assert calls == 2


async def test_with_retry_retries_on_504():
    client = make_client(max_retries=1, retry_delay=0.0)
    calls = 0

    async def fn():
        nonlocal calls
        calls += 1
        resp = MagicMock(status_code=504)
        raise httpx.HTTPStatusError("504", request=MagicMock(), response=resp)

    with patch("asyncio.sleep", AsyncMock()):
        with pytest.raises(httpx.HTTPStatusError):
            await client._with_retry(fn)

    assert calls == 2  # initial + 1 retry


async def test_with_retry_retries_on_network_error():
    client = make_client(max_retries=2, retry_delay=0.0)
    calls = 0

    async def fn():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise httpx.ConnectError("connection refused")
        return "ok"

    with patch("asyncio.sleep", AsyncMock()):
        result = await client._with_retry(fn)

    assert result == "ok"
    assert calls == 3


async def test_with_retry_does_not_retry_on_400():
    client = make_client(max_retries=3, retry_delay=0.0)
    calls = 0

    async def fn():
        nonlocal calls
        calls += 1
        resp = MagicMock(status_code=400)
        raise httpx.HTTPStatusError("400", request=MagicMock(), response=resp)

    with pytest.raises(httpx.HTTPStatusError):
        await client._with_retry(fn)

    assert calls == 1  # no retries


async def test_with_retry_does_not_retry_on_500():
    client = make_client(max_retries=3, retry_delay=0.0)
    calls = 0

    async def fn():
        nonlocal calls
        calls += 1
        resp = MagicMock(status_code=500)
        raise httpx.HTTPStatusError("500", request=MagicMock(), response=resp)

    with pytest.raises(httpx.HTTPStatusError):
        await client._with_retry(fn)

    assert calls == 1


async def test_with_retry_exponential_backoff():
    client = make_client(max_retries=3, retry_delay=1.0)
    sleep_calls = []

    async def fn():
        resp = MagicMock(status_code=502)
        raise httpx.HTTPStatusError("502", request=MagicMock(), response=resp)

    async def fake_sleep(seconds):
        sleep_calls.append(seconds)

    with patch("asyncio.sleep", fake_sleep):
        with pytest.raises(httpx.HTTPStatusError):
            await client._with_retry(fn)

    assert sleep_calls == [1.0, 2.0, 4.0]  # 1*2^0, 1*2^1, 1*2^2


async def test_with_retry_raises_after_max_retries():
    client = make_client(max_retries=2, retry_delay=0.0)

    async def fn():
        resp = MagicMock(status_code=503)
        raise httpx.HTTPStatusError("503", request=MagicMock(), response=resp)

    with patch("asyncio.sleep", AsyncMock()):
        with pytest.raises(httpx.HTTPStatusError):
            await client._with_retry(fn)


# --- post (response unwrapping) ---

async def test_post_unwraps_response_field():
    client = make_client()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": ["doc1", "doc2"]}
    mock_response.raise_for_status = MagicMock()

    mock_async_client = AsyncMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    mock_async_client.post = AsyncMock(return_value=mock_response)

    with patch("httpx.AsyncClient", return_value=mock_async_client):
        result = await client.post("api/test", {"key": "value"})

    assert result == ["doc1", "doc2"]


# --- download (raw bytes) ---

async def test_download_returns_raw_bytes():
    client = make_client()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"binary file data"
    mock_response.raise_for_status = MagicMock()

    mock_async_client = AsyncMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    mock_async_client.post = AsyncMock(return_value=mock_response)

    with patch("httpx.AsyncClient", return_value=mock_async_client):
        result = await client.download("api/document/download", {"id": "abc"})

    assert result == b"binary file data"
