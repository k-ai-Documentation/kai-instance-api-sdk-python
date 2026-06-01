# JS SDK Parity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the Python SDK to exact parity with the JavaScript SDK — same modules, methods, endpoints, retry logic, and credentials model. Breaking change.

**Architecture:** Replace the existing `Core`/`KaiStudioCredentials` files with a new `HttpClient` + `BaseModule` hierarchy. Four module classes (`Document`, `Orchestrator`, `SemanticGraph`, `KMAudit`) each extend `BaseModule`. `KaiInstanceApi` in `index.py` is the single factory entry point.

**Tech Stack:** Python 3.12, httpx 0.28.0, pytest, pytest-asyncio

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `tests/__init__.py` | test package |
| Create | `tests/test_http_client.py` | HttpClient retry + unwrap tests |
| Create | `tests/test_index.py` | KaiInstanceApi factory tests |
| Create | `tests/test_document.py` | Document module tests |
| Create | `tests/test_orchestrator.py` | Orchestrator module tests |
| Create | `tests/test_semantic_graph.py` | SemanticGraph module tests |
| Create | `tests/test_km_audit.py` | KMAudit module tests |
| Create | `pytest.ini` | asyncio_mode = auto |
| Create | `kai_sdk_python/modules/http_client.py` | HttpClient with retry |
| Create | `kai_sdk_python/modules/base_module.py` | BaseModule abstract |
| Create | `kai_sdk_python/modules/document.py` | Document module |
| Create | `kai_sdk_python/modules/orchestrator.py` | Orchestrator module |
| Rewrite | `kai_sdk_python/modules/semantic_graph.py` | SemanticGraph module |
| Rewrite | `kai_sdk_python/modules/km_audit.py` | KMAudit module |
| Rewrite | `kai_sdk_python/index.py` | KaiInstanceApi factory |
| Rewrite | `kai_sdk_python/__init__.py` | Public re-exports |
| Delete | `kai_sdk_python/modules/Core.py` | Replaced by Document + Orchestrator |
| Delete | `kai_sdk_python/modules/KaiStudioCredentials.py` | Merged into index.py |
| Rewrite | `example.py` | Uses new KaiInstanceApi |
| Modify | `setup.py` | Version bump, python_requires >=3.12, remove aiohttp |
| Modify | `CLAUDE.md` | Reflect actual new structure |

---

## Task 1: Test Infrastructure

**Files:**
- Create: `pytest.ini`
- Create: `tests/__init__.py`

- [ ] **Step 1: Install dev dependencies**

```bash
pip install pytest pytest-asyncio
```

Expected: packages install without error.

- [ ] **Step 2: Create `pytest.ini`**

```ini
[pytest]
asyncio_mode = auto
```

- [ ] **Step 3: Create `tests/__init__.py`**

Empty file:

```python
```

- [ ] **Step 4: Verify pytest is discovered**

```bash
pytest --collect-only
```

Expected: `no tests ran` (no tests yet, but no errors).

---

## Task 2: HttpClient

**Files:**
- Create: `kai_sdk_python/modules/http_client.py`
- Create: `tests/test_http_client.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_http_client.py`:

```python
import asyncio
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_http_client.py -v
```

Expected: `ImportError: cannot import name 'HttpClient'`

- [ ] **Step 3: Implement `http_client.py`**

Create `kai_sdk_python/modules/http_client.py`:

```python
import asyncio
from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class RetryOptions:
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 30.0


class HttpClient:
    RETRYABLE_STATUSES = {502, 503, 504}

    def __init__(self, headers: dict, base_url: str, retry_options: RetryOptions | None = None):
        self._headers = headers
        self._base_url = base_url
        opts = retry_options or RetryOptions()
        self._max_retries = opts.max_retries
        self._retry_delay = opts.retry_delay
        self._timeout = opts.timeout

    async def post(self, endpoint: str, data: dict | None = None) -> Any:
        return await self._with_retry(self._do_post, endpoint, data)

    async def download(self, endpoint: str, data: dict | None = None) -> bytes:
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
        raise last_error
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_http_client.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add kai_sdk_python/modules/http_client.py tests/test_http_client.py tests/__init__.py pytest.ini
git commit -m "feat: add HttpClient with exponential backoff retry logic"
```

---

## Task 3: BaseModule

**Files:**
- Create: `kai_sdk_python/modules/base_module.py`
- Create: `tests/test_base_module.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_base_module.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_base_module.py -v
```

Expected: `ImportError: cannot import name 'BaseModule'`

- [ ] **Step 3: Implement `base_module.py`**

Create `kai_sdk_python/modules/base_module.py`:

```python
from typing import Any

from .http_client import HttpClient, RetryOptions


class BaseModule:
    def __init__(self, headers: dict, base_url: str, retry_options: RetryOptions | None = None):
        self._http = HttpClient(headers, base_url, retry_options)

    async def _post(self, endpoint: str, data: dict | None = None) -> Any:
        return await self._http.post(endpoint, data)

    async def _download(self, endpoint: str, data: dict | None = None) -> bytes:
        return await self._http.download(endpoint, data)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_base_module.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add kai_sdk_python/modules/base_module.py tests/test_base_module.py
git commit -m "feat: add BaseModule abstract base with HttpClient delegation"
```

---

## Task 4: Entry Point (`index.py`)

**Files:**
- Rewrite: `kai_sdk_python/index.py`
- Create: `tests/test_index.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_index.py`:

```python
import pytest

from kai_sdk_python.index import KaiInstanceApi, KaiStudioCredentials, RetryOptions, State
from kai_sdk_python.modules.document import Document
from kai_sdk_python.modules.orchestrator import Orchestrator
from kai_sdk_python.modules.semantic_graph import SemanticGraph
from kai_sdk_python.modules.km_audit import KMAudit


def test_state_enum_values():
    assert State.PARSING_ERROR == "PARSING_ERROR"
    assert State.INITIAL_SAVED == "INITIAL_SAVED"
    assert State.UPDATED == "UPDATED"
    assert State.ON_CONTENT_EXTRACT == "ON_CONTENT_EXTRACT"
    assert State.CONTENT_EXTRACTED == "CONTENT_EXTRACTED"
    assert State.ON_INDEXATION == "ON_INDEXATION"
    assert State.INDEXED == "INDEXED"


def test_default_base_url():
    creds = KaiStudioCredentials(api_key="k", instance_id="i")
    api = KaiInstanceApi(creds)
    assert api.document()._http._base_url == "https://api.kai-studio.ai/"


def test_custom_host_overrides_base_url():
    creds = KaiStudioCredentials(host="https://my-server.example.com/")
    api = KaiInstanceApi(creds)
    assert api.document()._http._base_url == "https://my-server.example.com/"


def test_headers_include_api_key():
    creds = KaiStudioCredentials(api_key="my-key")
    api = KaiInstanceApi(creds)
    assert api.document()._http._headers.get("api-key") == "my-key"


def test_headers_include_instance_id():
    creds = KaiStudioCredentials(instance_id="my-instance")
    api = KaiInstanceApi(creds)
    assert api.document()._http._headers.get("instance-id") == "my-instance"


def test_headers_include_authorization():
    creds = KaiStudioCredentials(authorization="Bearer token123")
    api = KaiInstanceApi(creds)
    assert api.document()._http._headers.get("Authorization") == "Bearer token123"


def test_headers_include_api_host():
    creds = KaiStudioCredentials(api_host="proxy.example.com")
    api = KaiInstanceApi(creds)
    assert api.document()._http._headers.get("api-host") == "proxy.example.com"


def test_empty_credential_fields_excluded_from_headers():
    creds = KaiStudioCredentials(api_key="k")  # all others default to ""
    api = KaiInstanceApi(creds)
    headers = api.document()._http._headers
    assert "instance-id" not in headers
    assert "Authorization" not in headers
    assert "api-host" not in headers


def test_module_accessors_return_correct_types():
    creds = KaiStudioCredentials(api_key="k")
    api = KaiInstanceApi(creds)
    assert isinstance(api.document(), Document)
    assert isinstance(api.orchestrator(), Orchestrator)
    assert isinstance(api.semantic_graph(), SemanticGraph)
    assert isinstance(api.audit_instance(), KMAudit)


def test_module_accessors_return_same_instance():
    creds = KaiStudioCredentials(api_key="k")
    api = KaiInstanceApi(creds)
    assert api.document() is api.document()
    assert api.orchestrator() is api.orchestrator()
    assert api.semantic_graph() is api.semantic_graph()
    assert api.audit_instance() is api.audit_instance()


def test_get_credentials_returns_original():
    creds = KaiStudioCredentials(api_key="k", instance_id="i")
    api = KaiInstanceApi(creds)
    assert api.get_credentials() is creds


def test_retry_options_forwarded_to_modules():
    creds = KaiStudioCredentials(api_key="k")
    opts = RetryOptions(max_retries=5, retry_delay=2.0, timeout=60.0)
    api = KaiInstanceApi(creds, opts)
    assert api.document()._http._max_retries == 5
    assert api.document()._http._retry_delay == 2.0
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_index.py -v
```

Expected: `ImportError: cannot import name 'KaiInstanceApi'`

- [ ] **Step 3: Implement `index.py`**

Overwrite `kai_sdk_python/index.py`:

```python
from dataclasses import dataclass, field
from enum import Enum

from .modules.http_client import RetryOptions
from .modules.document import Document
from .modules.orchestrator import Orchestrator
from .modules.semantic_graph import SemanticGraph
from .modules.km_audit import KMAudit


class State(str, Enum):
    PARSING_ERROR = "PARSING_ERROR"
    INITIAL_SAVED = "INITIAL_SAVED"
    UPDATED = "UPDATED"
    ON_CONTENT_EXTRACT = "ON_CONTENT_EXTRACT"
    CONTENT_EXTRACTED = "CONTENT_EXTRACTED"
    ON_INDEXATION = "ON_INDEXATION"
    INDEXED = "INDEXED"


@dataclass
class KaiStudioCredentials:
    api_key: str = ""
    instance_id: str = ""
    host: str = ""
    authorization: str = ""
    api_host: str = ""


class KaiInstanceApi:
    def __init__(self, credentials: KaiStudioCredentials, retry_options: RetryOptions | None = None):
        self._credentials = credentials
        headers = {}
        if credentials.api_key:
            headers["api-key"] = credentials.api_key
        if credentials.instance_id:
            headers["instance-id"] = credentials.instance_id
        if credentials.authorization:
            headers["Authorization"] = credentials.authorization
        if credentials.api_host:
            headers["api-host"] = credentials.api_host

        base_url = credentials.host or "https://api.kai-studio.ai/"

        self._document = Document(headers, base_url, retry_options)
        self._orchestrator = Orchestrator(headers, base_url, retry_options)
        self._semantic_graph = SemanticGraph(headers, base_url, retry_options)
        self._audit_instance = KMAudit(headers, base_url, retry_options)

    def document(self) -> Document:
        return self._document

    def orchestrator(self) -> Orchestrator:
        return self._orchestrator

    def semantic_graph(self) -> SemanticGraph:
        return self._semantic_graph

    def audit_instance(self) -> KMAudit:
        return self._audit_instance

    def get_credentials(self) -> KaiStudioCredentials:
        return self._credentials
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_index.py -v
```

Expected: all tests PASS. (Note: Document, Orchestrator, SemanticGraph, KMAudit must exist for imports to work — stub them if needed, or implement them in order in the next tasks. If you get ImportError for those, add temporary empty class stubs and remove them after the module tasks are done.)

- [ ] **Step 5: Commit**

```bash
git add kai_sdk_python/index.py tests/test_index.py
git commit -m "feat: add KaiInstanceApi factory, KaiStudioCredentials, State enum"
```

---

## Task 5: Document Module

**Files:**
- Create: `kai_sdk_python/modules/document.py`
- Create: `tests/test_document.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_document.py`:

```python
from unittest.mock import AsyncMock
import pytest

from kai_sdk_python.modules.document import Document


def make_module():
    return Document({"api-key": "k"}, "https://api.example.com/")


async def test_list_documents_default_params():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.list_documents()
    m._post.assert_called_once_with("api/document/list-docs", {"offset": 0, "limit": 20, "state": None})


async def test_list_documents_custom_params():
    m = make_module()
    m._post = AsyncMock(return_value=[{"id": "doc1"}])
    result = await m.list_documents(offset=5, limit=10, state="INDEXED")
    m._post.assert_called_once_with("api/document/list-docs", {"offset": 5, "limit": 10, "state": "INDEXED"})
    assert result == [{"id": "doc1"}]


async def test_get_document_detail():
    m = make_module()
    m._post = AsyncMock(return_value={"id": "doc1", "name": "My Doc"})
    result = await m.get_document_detail("doc1")
    m._post.assert_called_once_with("api/document/doc", {"id": "doc1"})
    assert result["id"] == "doc1"


async def test_count_documents_no_params():
    m = make_module()
    m._post = AsyncMock(return_value=42)
    result = await m.count_documents()
    m._post.assert_called_once_with("api/document/count-documents", {})
    assert result == 42


async def test_count_documents_with_state():
    m = make_module()
    m._post = AsyncMock(return_value=10)
    await m.count_documents(state="INDEXED")
    m._post.assert_called_once_with("api/document/count-documents", {"state": "INDEXED"})


async def test_count_documents_with_document_ids():
    m = make_module()
    m._post = AsyncMock(return_value=3)
    await m.count_documents(document_ids=["a", "b", "c"])
    m._post.assert_called_once_with("api/document/count-documents", {"document_ids": ["a", "b", "c"]})


async def test_count_documents_with_state_and_ids():
    m = make_module()
    m._post = AsyncMock(return_value=2)
    await m.count_documents(state="INDEXED", document_ids=["a", "b"])
    m._post.assert_called_once_with(
        "api/document/count-documents",
        {"state": "INDEXED", "document_ids": ["a", "b"]}
    )


async def test_download_file():
    m = make_module()
    m._download = AsyncMock(return_value=b"binary data")
    result = await m.download_file("doc123")
    m._download.assert_called_once_with("api/document/download", {"id": "doc123"})
    assert result == b"binary data"


async def test_docs_by_ids_default_pagination():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.docs_by_ids(["id1", "id2"])
    m._post.assert_called_once_with("api/document/docs-by-ids", {"ids": ["id1", "id2"], "offset": 0, "limit": 20})


async def test_docs_by_ids_custom_pagination():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.docs_by_ids(["id1"], offset=5, limit=50)
    m._post.assert_called_once_with("api/document/docs-by-ids", {"ids": ["id1"], "offset": 5, "limit": 50})
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_document.py -v
```

Expected: `ImportError: cannot import name 'Document'`

- [ ] **Step 3: Implement `document.py`**

Create `kai_sdk_python/modules/document.py`:

```python
from typing import TypedDict

from .base_module import BaseModule


class DocumentSignatureExtraproperties(TypedDict):
    audit_done: bool
    kb_signature: dict[str, str]
    kai_internal_state: str
    kai_internal_count_chunks: int


class DocumentSignature(TypedDict):
    id: str
    name: str
    url: str | None
    extraproperties: DocumentSignatureExtraproperties


class Document(BaseModule):
    async def list_documents(
        self,
        offset: int = 0,
        limit: int = 20,
        state: str | None = None,
    ) -> list[DocumentSignature]:
        return await self._post("api/document/list-docs", {"offset": offset, "limit": limit, "state": state})

    async def get_document_detail(self, id: str) -> DocumentSignature | None:
        return await self._post("api/document/doc", {"id": id})

    async def count_documents(
        self,
        state: str | None = None,
        document_ids: list[str] | None = None,
    ) -> int:
        payload: dict = {}
        if state is not None:
            payload["state"] = state
        if document_ids is not None:
            payload["document_ids"] = document_ids
        return await self._post("api/document/count-documents", payload)

    async def download_file(self, document_id: str) -> bytes:
        return await self._download("api/document/download", {"id": document_id})

    async def docs_by_ids(
        self,
        ids: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[DocumentSignature]:
        return await self._post("api/document/docs-by-ids", {"ids": ids, "offset": offset, "limit": limit})
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_document.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add kai_sdk_python/modules/document.py tests/test_document.py
git commit -m "feat: add Document module (list, detail, count, download, docs-by-ids)"
```

---

## Task 6: Orchestrator Module

**Files:**
- Create: `kai_sdk_python/modules/orchestrator.py`
- Create: `tests/test_orchestrator.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_orchestrator.py`:

```python
from unittest.mock import AsyncMock
import pytest

from kai_sdk_python.modules.orchestrator import Orchestrator


def make_module():
    return Orchestrator({"api-key": "k"}, "https://api.example.com/")


async def test_launch_partial_indexation():
    m = make_module()
    m._post = AsyncMock(return_value=True)
    result = await m.launch_partial_indexation()
    m._post.assert_called_once_with("api/orchestrator/differential-indexation", {})
    assert result is True


async def test_reindex_document():
    m = make_module()
    m._post = AsyncMock(return_value=True)
    result = await m.reindex_document("doc123")
    m._post.assert_called_once_with("api/orchestrator/reindex-document", {"id": "doc123"})
    assert result is True


async def test_retry_index_error_parsing_documents():
    m = make_module()
    m._post = AsyncMock(return_value=True)
    result = await m.retry_index_error_parsing_documents()
    m._post.assert_called_once_with("api/orchestrator/retry-documents-parsing-error", {})
    assert result is True


async def test_count_registered_background_tasks():
    m = make_module()
    m._post = AsyncMock(return_value={"indexation": 3})
    result = await m.count_registered_background_tasks()
    m._post.assert_called_once_with("api/orchestrator/count-back-tasks", {})
    assert result == {"indexation": 3}


async def test_count_registered_background_tasks_for_doc():
    m = make_module()
    m._post = AsyncMock(return_value={"indexation": 1})
    result = await m.count_registered_background_tasks_for_doc("doc456")
    m._post.assert_called_once_with("api/orchestrator/count-tasks-for-doc", {"id": "doc456"})
    assert result == {"indexation": 1}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_orchestrator.py -v
```

Expected: `ImportError: cannot import name 'Orchestrator'`

- [ ] **Step 3: Implement `orchestrator.py`**

Create `kai_sdk_python/modules/orchestrator.py`:

```python
from .base_module import BaseModule


class Orchestrator(BaseModule):
    async def launch_partial_indexation(self) -> bool:
        return await self._post("api/orchestrator/differential-indexation", {})

    async def reindex_document(self, document_id: str) -> bool:
        return await self._post("api/orchestrator/reindex-document", {"id": document_id})

    async def retry_index_error_parsing_documents(self) -> bool:
        return await self._post("api/orchestrator/retry-documents-parsing-error", {})

    async def count_registered_background_tasks(self) -> dict[str, int]:
        return await self._post("api/orchestrator/count-back-tasks", {})

    async def count_registered_background_tasks_for_doc(self, document_id: str) -> dict[str, int]:
        return await self._post("api/orchestrator/count-tasks-for-doc", {"id": document_id})
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_orchestrator.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add kai_sdk_python/modules/orchestrator.py tests/test_orchestrator.py
git commit -m "feat: add Orchestrator module (indexation triggers, background task counts)"
```

---

## Task 7: SemanticGraph Module

**Files:**
- Rewrite: `kai_sdk_python/modules/semantic_graph.py`
- Create: `tests/test_semantic_graph.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_semantic_graph.py`:

```python
from unittest.mock import AsyncMock
import pytest

from kai_sdk_python.modules.semantic_graph import SemanticGraph


def make_module():
    return SemanticGraph({"api-key": "k"}, "https://api.example.com/")


async def test_get_nodes_defaults():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_nodes()
    m._post.assert_called_once_with("api/semantic-graph/nodes", {"limit": 20, "offset": 0})


async def test_get_nodes_custom():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_nodes(limit=50, offset=10)
    m._post.assert_called_once_with("api/semantic-graph/nodes", {"limit": 50, "offset": 10})


async def test_get_node_by_label():
    m = make_module()
    m._post = AsyncMock(return_value=[{"id": "n1"}])
    result = await m.get_node_by_label("Python")
    m._post.assert_called_once_with("api/semantic-graph/nodes-by-label", {"label": "Python"})
    assert result == [{"id": "n1"}]


async def test_identify_nodes_default_content_flag():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.identify_nodes("what is Python?")
    m._post.assert_called_once_with(
        "api/semantic-graph/identify-nodes",
        {"query": "what is Python?", "need_documents_content": False}
    )


async def test_identify_nodes_with_content():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.identify_nodes("what is Python?", need_documents_content=True)
    m._post.assert_called_once_with(
        "api/semantic-graph/identify-nodes",
        {"query": "what is Python?", "need_documents_content": True}
    )


async def test_linked_nodes_by_id():
    m = make_module()
    m._post = AsyncMock(return_value=[{"id": "n2"}])
    result = await m.linked_nodes_by_id("node123")
    m._post.assert_called_once_with("api/semantic-graph/linked-nodes-by-id", {"id": "node123"})
    assert result == [{"id": "n2"}]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_semantic_graph.py -v
```

Expected: tests fail (either import error or missing methods on old implementation).

- [ ] **Step 3: Rewrite `semantic_graph.py`**

Overwrite `kai_sdk_python/modules/semantic_graph.py` entirely:

```python
from typing import TypedDict

from .base_module import BaseModule


class SemanticNodeExtraproperties(TypedDict):
    documents: list[str]
    chunks: list[str]
    count: int


class SemanticNode(TypedDict):
    id: str
    node_1: str
    node_2: str
    edge: str
    extraproperties: SemanticNodeExtraproperties


class PartialDocument(TypedDict):
    id: str
    content: list[str]


class IdentifiedNode(TypedDict):
    id: str
    node1: str
    node2: str
    edge: str
    documents: list[PartialDocument] | list[str]


class SemanticGraph(BaseModule):
    async def get_nodes(self, limit: int = 20, offset: int = 0) -> list[SemanticNode]:
        return await self._post("api/semantic-graph/nodes", {"limit": limit, "offset": offset})

    async def get_node_by_label(self, label: str) -> list[SemanticNode]:
        return await self._post("api/semantic-graph/nodes-by-label", {"label": label})

    async def identify_nodes(
        self,
        query: str,
        need_documents_content: bool = False,
    ) -> list[IdentifiedNode]:
        return await self._post(
            "api/semantic-graph/identify-nodes",
            {"query": query, "need_documents_content": need_documents_content},
        )

    async def linked_nodes_by_id(self, id: str) -> list[SemanticNode]:
        return await self._post("api/semantic-graph/linked-nodes-by-id", {"id": id})
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_semantic_graph.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add kai_sdk_python/modules/semantic_graph.py tests/test_semantic_graph.py
git commit -m "feat: rewrite SemanticGraph module to match JS SDK (identify_nodes, linked_nodes_by_id)"
```

---

## Task 8: KMAudit Module

**Files:**
- Rewrite: `kai_sdk_python/modules/km_audit.py`
- Create: `tests/test_km_audit.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_km_audit.py`:

```python
from unittest.mock import AsyncMock
import pytest

from kai_sdk_python.modules.km_audit import KMAudit, AnomalyState


def make_module():
    return KMAudit({"api-key": "k"}, "https://api.example.com/")


async def test_update_conflict_state():
    m = make_module()
    m._post = AsyncMock(return_value=True)
    result = await m.update_conflict_state("anomaly1", AnomalyState.MANAGED)
    m._post.assert_called_once_with(
        "api/audit/conflict-information/set-state",
        {"id": "anomaly1", "state": AnomalyState.MANAGED}
    )
    assert result is True


async def test_count_conflicts():
    m = make_module()
    m._post = AsyncMock(return_value=15)
    result = await m.count_conflicts()
    m._post.assert_called_once_with("api/audit/count-conflict-information", {})
    assert result == 15


async def test_list_conflicts_defaults():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.list_conflicts()
    m._post.assert_called_once_with(
        "api/audit/conflict-information",
        {"limit": 200, "offset": 0, "query": None, "document_name": None, "state": None}
    )


async def test_list_conflicts_with_filters():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.list_conflicts(limit=50, offset=10, query="python", document_name="guide.pdf", state=AnomalyState.DETECTED)
    m._post.assert_called_once_with(
        "api/audit/conflict-information",
        {"limit": 50, "offset": 10, "query": "python", "document_name": "guide.pdf", "state": AnomalyState.DETECTED}
    )


async def test_count_anomalies_per_document_defaults():
    m = make_module()
    m._post = AsyncMock(return_value={})
    await m.count_anomalies_per_document()
    m._post.assert_called_once_with("api/audit/document-ids-to-manage", {"limit": 20, "offset": 0, "document_ids": None})


async def test_count_anomalies_per_document_with_ids():
    m = make_module()
    m._post = AsyncMock(return_value={})
    await m.count_anomalies_per_document(document_ids=["a", "b"])
    m._post.assert_called_once_with(
        "api/audit/document-ids-to-manage",
        {"limit": 20, "offset": 0, "document_ids": ["a", "b"]}
    )


async def test_get_anomalies_for_document():
    m = make_module()
    m._post = AsyncMock(return_value={"conflicts": []})
    result = await m.get_anomalies_for_document("doc1")
    m._post.assert_called_once_with("api/audit/get-anomalies-for-document", {"id": "doc1"})
    assert result == {"conflicts": []}


async def test_count_conflicts_for_period_no_state():
    m = make_module()
    m._post = AsyncMock(return_value={})
    await m.count_conflicts_for_period("2026-01-01", "2026-01-31")
    m._post.assert_called_once_with(
        "api/audit/count-conflict-by-date",
        {"begin_date": "2026-01-01", "end_date": "2026-01-31", "state": None}
    )


async def test_count_conflicts_by_state():
    m = make_module()
    m._post = AsyncMock(return_value=7)
    result = await m.count_conflicts_by_state(AnomalyState.DETECTED)
    m._post.assert_called_once_with("api/audit/count-conflicts-by-state", {"state": AnomalyState.DETECTED})
    assert result == 7


async def test_get_conflict_document_pairs_defaults():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_conflict_document_pairs()
    m._post.assert_called_once_with(
        "api/audit/get-conflict-document-pair",
        {"limit": 200, "offset": 0, "document_name": None, "state": None, "order": None}
    )


async def test_get_conflicts_by_document_pair_no_state():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_conflicts_by_document_pair(["docA", "docB"])
    m._post.assert_called_once_with(
        "api/audit/get-conflicts-by-document-id-pair",
        {"document_ids": ["docA", "docB"], "limit": 200, "offset": 0}
    )


async def test_get_conflicts_by_document_pair_with_state():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_conflicts_by_document_pair(["docA", "docB"], state=AnomalyState.MANAGED)
    call_args = m._post.call_args
    assert call_args[0][1]["state"] == AnomalyState.MANAGED


async def test_count_conflicts_per_subject_parses_string_counts():
    m = make_module()
    m._post = AsyncMock(return_value=[
        {
            "subject": "topic A",
            "count": "5",
            "count_detected": "2",
            "count_managed": "1",
            "count_ignored": "1",
            "count_redetected": "0",
            "count_disappeared": "1",
        }
    ])
    result = await m.count_conflicts_per_subject()
    assert result[0]["count"] == 5
    assert result[0]["count_detected"] == 2
    assert isinstance(result[0]["count"], int)
    assert isinstance(result[0]["count_disappeared"], int)


async def test_count_conflicts_per_subject_with_document_ids():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.count_conflicts_per_subject(document_ids=["d1"])
    m._post.assert_called_once_with("api/audit/count-conflict-by-subject", {"document_ids": ["d1"]})


async def test_get_conflicts_by_subject_defaults():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_conflicts_by_subject()
    m._post.assert_called_once_with(
        "api/audit/get-conflict-information-by-subject",
        {"subject": None, "offset": 0, "limit": 50}
    )


async def test_check_if_document_is_audited():
    m = make_module()
    m._post = AsyncMock(return_value=True)
    result = await m.check_if_document_is_audited("doc1")
    m._post.assert_called_once_with("api/audit/document-is-analyzed", {"id": "doc1"})
    assert result is True


async def test_count_conflicts_by_document_id_parses_string():
    m = make_module()
    m._post = AsyncMock(return_value="12")
    result = await m.count_conflicts_by_document_id(["docA", "docB"])
    m._post.assert_called_once_with(
        "api/audit/count-conflict-by-document-ids",
        {"document_ids": ["docA", "docB"], "state": None}
    )
    assert result == 12
    assert isinstance(result, int)


async def test_count_conflicts_by_document_id_with_state():
    m = make_module()
    m._post = AsyncMock(return_value="3")
    result = await m.count_conflicts_by_document_id(["docA"], state=AnomalyState.MANAGED)
    call_args = m._post.call_args
    assert call_args[0][1]["state"] == AnomalyState.MANAGED
    assert result == 3
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_km_audit.py -v
```

Expected: tests fail (import errors or missing methods).

- [ ] **Step 3: Rewrite `km_audit.py`**

Overwrite `kai_sdk_python/modules/km_audit.py` entirely:

```python
from enum import Enum
from typing import TypedDict

from .base_module import BaseModule


class AnomalyState(str, Enum):
    MANAGED = "managed"
    IGNORED = "ignored"
    DETECTED = "detected"
    REDETECTED = "redetected"
    DISAPPEARED = "disappeared"


class AnomalyInformationDocument(TypedDict):
    doc_id: str
    information_involved: str


class Anomaly(TypedDict):
    id: str
    subject: str
    state: AnomalyState
    documents: list[AnomalyInformationDocument]
    explanation: str


class DocumentAnomalies(TypedDict):
    conflicts: list[Anomaly]


class AnomalyTypeNumber(TypedDict):
    subject: str
    count: int
    count_detected: int
    count_managed: int
    count_ignored: int
    count_redetected: int
    count_disappeared: int


class ConflictDocumentPair(TypedDict):
    document_ids: list[str]
    conflict_count: int
    state: str


class KMAudit(BaseModule):
    async def update_conflict_state(self, id: str, state: AnomalyState) -> bool:
        return await self._post("api/audit/conflict-information/set-state", {"id": id, "state": state})

    async def count_conflicts(self) -> int:
        return await self._post("api/audit/count-conflict-information", {})

    async def list_conflicts(
        self,
        limit: int = 200,
        offset: int = 0,
        query: str | None = None,
        document_name: str | None = None,
        state: AnomalyState | None = None,
    ) -> list[Anomaly]:
        return await self._post(
            "api/audit/conflict-information",
            {"limit": limit, "offset": offset, "query": query, "document_name": document_name, "state": state},
        )

    async def count_anomalies_per_document(
        self,
        limit: int = 20,
        offset: int = 0,
        document_ids: list[str] | None = None,
    ) -> dict[str, dict[str, int]]:
        return await self._post(
            "api/audit/document-ids-to-manage",
            {"limit": limit, "offset": offset, "document_ids": document_ids},
        )

    async def get_anomalies_for_document(self, document_id: str) -> DocumentAnomalies:
        return await self._post("api/audit/get-anomalies-for-document", {"id": document_id})

    async def count_conflicts_for_period(
        self,
        begin_date: str,
        end_date: str,
        state: AnomalyState | None = None,
    ) -> dict[str, dict[str, int]]:
        return await self._post(
            "api/audit/count-conflict-by-date",
            {"begin_date": begin_date, "end_date": end_date, "state": state},
        )

    async def count_conflicts_by_state(self, state: AnomalyState) -> int:
        return await self._post("api/audit/count-conflicts-by-state", {"state": state})

    async def get_conflict_document_pairs(
        self,
        limit: int = 200,
        offset: int = 0,
        document_name: str | None = None,
        state: str | None = None,
        sort_order: str | None = None,
    ) -> list[ConflictDocumentPair]:
        return await self._post(
            "api/audit/get-conflict-document-pair",
            {"limit": limit, "offset": offset, "document_name": document_name, "state": state, "order": sort_order},
        )

    async def get_conflicts_by_document_pair(
        self,
        document_ids: list[str],
        limit: int = 200,
        offset: int = 0,
        state: AnomalyState | None = None,
    ) -> list[Anomaly]:
        payload: dict = {"document_ids": document_ids, "limit": limit, "offset": offset}
        if state is not None:
            payload["state"] = state
        return await self._post("api/audit/get-conflicts-by-document-id-pair", payload)

    async def count_conflicts_per_subject(
        self,
        document_ids: list[str] | None = None,
    ) -> list[AnomalyTypeNumber]:
        payload: dict = {}
        if document_ids is not None:
            payload["document_ids"] = document_ids
        raw: list = await self._post("api/audit/count-conflict-by-subject", payload)
        return [
            {
                "subject": item["subject"],
                "count": int(item["count"]),
                "count_detected": int(item["count_detected"]),
                "count_managed": int(item["count_managed"]),
                "count_ignored": int(item["count_ignored"]),
                "count_redetected": int(item["count_redetected"]),
                "count_disappeared": int(item["count_disappeared"]),
            }
            for item in raw
        ]

    async def get_conflicts_by_subject(
        self,
        subject: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> list[Anomaly]:
        return await self._post(
            "api/audit/get-conflict-information-by-subject",
            {"subject": subject, "offset": offset, "limit": limit},
        )

    async def check_if_document_is_audited(self, document_id: str) -> bool:
        return await self._post("api/audit/document-is-analyzed", {"id": document_id})

    async def count_conflicts_by_document_id(
        self,
        document_ids: list[str],
        state: AnomalyState | None = None,
    ) -> int:
        raw: str = await self._post(
            "api/audit/count-conflict-by-document-ids",
            {"document_ids": document_ids, "state": state},
        )
        return int(raw)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_km_audit.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add kai_sdk_python/modules/km_audit.py tests/test_km_audit.py
git commit -m "feat: rewrite KMAudit with 13 methods matching JS SDK"
```

---

## Task 9: Clean Up Old Files & Update `__init__.py`

**Files:**
- Delete: `kai_sdk_python/modules/Core.py`
- Delete: `kai_sdk_python/modules/KaiStudioCredentials.py`
- Rewrite: `kai_sdk_python/__init__.py`
- Modify: `kai_sdk_python/modules/__init__.py`

- [ ] **Step 1: Delete old files**

```bash
git rm kai_sdk_python/modules/Core.py kai_sdk_python/modules/KaiStudioCredentials.py
```

- [ ] **Step 2: Run full test suite to confirm nothing broke**

```bash
pytest -v
```

Expected: all tests PASS (removed files should not be imported by any remaining code).

- [ ] **Step 3: Update `kai_sdk_python/__init__.py`**

Overwrite with:

```python
from .index import KaiInstanceApi, KaiStudioCredentials, State
from .modules.http_client import RetryOptions
from .modules.document import Document, DocumentSignature
from .modules.orchestrator import Orchestrator
from .modules.semantic_graph import SemanticGraph, SemanticNode, IdentifiedNode
from .modules.km_audit import KMAudit, AnomalyState, Anomaly, DocumentAnomalies

__all__ = [
    "KaiInstanceApi",
    "KaiStudioCredentials",
    "RetryOptions",
    "State",
    "Document",
    "DocumentSignature",
    "Orchestrator",
    "SemanticGraph",
    "SemanticNode",
    "IdentifiedNode",
    "KMAudit",
    "AnomalyState",
    "Anomaly",
    "DocumentAnomalies",
]
```

- [ ] **Step 4: Run full test suite again**

```bash
pytest -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add kai_sdk_python/__init__.py kai_sdk_python/modules/__init__.py
git commit -m "chore: remove old Core.py and KaiStudioCredentials.py, update __init__ exports"
```

---

## Task 10: Rewrite `example.py`

**Files:**
- Rewrite: `example.py`

- [ ] **Step 1: Overwrite `example.py`**

```python
import asyncio

from kai_sdk_python import KaiInstanceApi, KaiStudioCredentials, RetryOptions, State, AnomalyState

credentials = KaiStudioCredentials(
    api_key="your-api-key",
    instance_id="your-instance-id",
)

# Optional: configure retry and timeout behavior
retry_options = RetryOptions(max_retries=3, retry_delay=1.0, timeout=30.0)

api = KaiInstanceApi(credentials, retry_options)


async def demo_document():
    doc = api.document()

    print("LIST DOCUMENTS")
    print(await doc.list_documents(offset=0, limit=5))

    print("COUNT ALL DOCUMENTS")
    print(await doc.count_documents())

    print("COUNT INDEXED DOCUMENTS")
    print(await doc.count_documents(state=State.INDEXED))

    print("COUNT DOCUMENTS BY IDS")
    print(await doc.count_documents(document_ids=["doc-id-1", "doc-id-2"]))

    print("GET DOCUMENT DETAIL")
    print(await doc.get_document_detail("your-document-id"))

    print("DOCS BY IDS")
    print(await doc.docs_by_ids(["doc-id-1", "doc-id-2"]))

    print("DOWNLOAD FILE")
    data = await doc.download_file("your-document-id")
    print(f"Downloaded {len(data)} bytes")


async def demo_orchestrator():
    orch = api.orchestrator()

    print("LAUNCH PARTIAL INDEXATION")
    print(await orch.launch_partial_indexation())

    print("REINDEX DOCUMENT")
    print(await orch.reindex_document("your-document-id"))

    print("RETRY PARSING ERRORS")
    print(await orch.retry_index_error_parsing_documents())

    print("COUNT BACKGROUND TASKS")
    print(await orch.count_registered_background_tasks())

    print("COUNT BACKGROUND TASKS FOR DOC")
    print(await orch.count_registered_background_tasks_for_doc("your-document-id"))


async def demo_semantic_graph():
    sg = api.semantic_graph()

    print("GET NODES")
    print(await sg.get_nodes(limit=10, offset=0))

    print("GET NODE BY LABEL")
    print(await sg.get_node_by_label("Python"))

    print("IDENTIFY NODES")
    print(await sg.identify_nodes("what is machine learning?"))

    print("IDENTIFY NODES WITH CONTENT")
    print(await sg.identify_nodes("what is machine learning?", need_documents_content=True))

    print("LINKED NODES BY ID")
    print(await sg.linked_nodes_by_id("your-node-id"))


async def demo_audit():
    audit = api.audit_instance()

    print("COUNT CONFLICTS")
    print(await audit.count_conflicts())

    print("LIST CONFLICTS")
    print(await audit.list_conflicts(limit=10))

    print("LIST CONFLICTS WITH FILTERS")
    print(await audit.list_conflicts(query="python", state=AnomalyState.DETECTED))

    print("UPDATE CONFLICT STATE")
    print(await audit.update_conflict_state("anomaly-id", AnomalyState.MANAGED))

    print("COUNT ANOMALIES PER DOCUMENT")
    print(await audit.count_anomalies_per_document(limit=10))

    print("GET ANOMALIES FOR DOCUMENT")
    print(await audit.get_anomalies_for_document("your-document-id"))

    print("COUNT CONFLICTS FOR PERIOD")
    print(await audit.count_conflicts_for_period("2026-01-01", "2026-06-01"))

    print("COUNT CONFLICTS BY STATE")
    print(await audit.count_conflicts_by_state(AnomalyState.DETECTED))

    print("GET CONFLICT DOCUMENT PAIRS")
    print(await audit.get_conflict_document_pairs(limit=10))

    print("GET CONFLICTS BY DOCUMENT PAIR")
    print(await audit.get_conflicts_by_document_pair(["doc-id-1", "doc-id-2"]))

    print("COUNT CONFLICTS PER SUBJECT")
    print(await audit.count_conflicts_per_subject())

    print("GET CONFLICTS BY SUBJECT")
    print(await audit.get_conflicts_by_subject(subject="machine learning"))

    print("CHECK IF DOCUMENT IS AUDITED")
    print(await audit.check_if_document_is_audited("your-document-id"))

    print("COUNT CONFLICTS BY DOCUMENT ID")
    print(await audit.count_conflicts_by_document_id(["doc-id-1", "doc-id-2"]))


if __name__ == "__main__":
    asyncio.run(demo_document())
    asyncio.run(demo_orchestrator())
    asyncio.run(demo_semantic_graph())
    asyncio.run(demo_audit())
```

- [ ] **Step 2: Verify the file parses cleanly**

```bash
python -c "import ast; ast.parse(open('example.py').read()); print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add example.py
git commit -m "chore: rewrite example.py to use KaiInstanceApi"
```

---

## Task 11: Update `setup.py` and `CLAUDE.md`

**Files:**
- Modify: `setup.py`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update `setup.py`**

Overwrite with:

```python
import setuptools

setuptools.setup(
    name="kai_sdk_python",
    version="20260601",
    author="KAI",
    author_email="support@wats.ai",
    description="KAI Studio Python SDK",
    packages=setuptools.find_packages(),
    install_requires=["httpx==0.28.0"],
    python_requires=">=3.12",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/k-ai-Documentation/kai-instance-api-sdk-python",
)
```

- [ ] **Step 2: Update `CLAUDE.md`**

Replace the Architecture and Modules sections with:

````markdown
## Architecture

The SDK is a Python 3.12 async client for the **KAI Studio** platform.

### Entry Point

`KaiInstanceApi` (`kai_sdk_python/index.py`) is the factory class. Instantiate it with `KaiStudioCredentials`, then call getter methods to access modules:

```python
from kai_sdk_python import KaiInstanceApi, KaiStudioCredentials, RetryOptions

credentials = KaiStudioCredentials(api_key="...", instance_id="...")
api = KaiInstanceApi(credentials, RetryOptions(max_retries=3, timeout=30.0))

api.document()         # Document management
api.orchestrator()     # Indexation triggers and background tasks
api.semantic_graph()   # Knowledge graph queries
api.audit_instance()   # Conflict anomaly management
```

### Credentials & Base URLs

`KaiStudioCredentials` fields (all optional strings, default `""`):

- `api_key` → `api-key` header
- `instance_id` → `instance-id` header
- `authorization` → `Authorization` header
- `api_host` → `api-host` header
- `host` → overrides base URL (default: `https://api.kai-studio.ai/`)

Only non-empty fields are sent as headers.

### Modules

| Module | File | Responsibility |
|--------|------|----------------|
| `Document` | `modules/document.py` | Document listing, detail, count, download |
| `Orchestrator` | `modules/orchestrator.py` | Indexation triggers, background task monitoring |
| `SemanticGraph` | `modules/semantic_graph.py` | Knowledge graph node queries |
| `KMAudit` | `modules/km_audit.py` | Conflict anomaly detection and management |

### Infrastructure

| File | Responsibility |
|------|----------------|
| `modules/http_client.py` | `HttpClient` — httpx wrapper with exponential backoff retry on 502/503/504 and network errors |
| `modules/base_module.py` | `BaseModule` — abstract parent for all modules, delegates to `HttpClient` |

### Retry Logic

`HttpClient` retries on HTTP 502, 503, 504, and `httpx.RequestError` (network errors). Backoff formula: `retry_delay * 2^attempt`. Non-retryable statuses (4xx, 500) fail immediately. All standard responses are unwrapped from `response.json()["response"]`. The `download()` method returns raw `bytes`.

### State Enum

Document lifecycle states (defined in `index.py`):

```
PARSING_ERROR → INITIAL_SAVED → UPDATED → ON_CONTENT_EXTRACT
             → CONTENT_EXTRACTED → ON_INDEXATION → INDEXED
```

### Async Pattern

All API methods are `async def` using `httpx.AsyncClient`. Callers must use `asyncio.run()` or an existing event loop.
````

- [ ] **Step 3: Run full test suite one final time**

```bash
pytest -v
```

Expected: all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add setup.py CLAUDE.md
git commit -m "chore: bump version to 20260601, update CLAUDE.md to reflect new SDK structure"
```

---

## Self-Review

**Spec coverage:**
- ✅ `HttpClient` with retry, backoff, response unwrapping, download
- ✅ `BaseModule`
- ✅ `KaiStudioCredentials`, `RetryOptions`, `State` enum, `KaiInstanceApi`
- ✅ `Document` — all 5 methods
- ✅ `Orchestrator` — all 5 methods
- ✅ `SemanticGraph` — all 4 methods (including `linked_nodes_by_id` replacing old `get_linked_nodes`)
- ✅ `KMAudit` — all 13 methods (including string→int parsing for `count_conflicts_per_subject` and `count_conflicts_by_document_id`)
- ✅ Delete `Core.py`, `KaiStudioCredentials.py`
- ✅ `example.py` rewritten
- ✅ `setup.py` version bumped, `aiohttp` removed, `python_requires >=3.12`
- ✅ `CLAUDE.md` updated

**Placeholder scan:** No TBDs. All code steps are complete. All test assertions reference actual method names defined in implementation steps.

**Type consistency:** `_post` and `_download` naming is consistent across `HttpClient`, `BaseModule`, and all module classes. `AnomalyState` is used in both `KMAudit` methods and tests. `DocumentSignature` is defined in `document.py` and referenced correctly.
