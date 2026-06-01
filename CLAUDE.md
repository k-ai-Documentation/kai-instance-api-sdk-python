# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
pip install pytest pytest-asyncio
```

The only runtime dependency is `httpx==0.28.0`. Python 3.12+ is required.

## Running Tests

```bash
pytest
```

## Running Examples

```bash
python example.py
```

To use the SDK manually:

```python
import asyncio
from kai_sdk_python import KaiInstanceApi, KaiStudioCredentials

credentials = KaiStudioCredentials(api_key="...", instance_id="...")
api = KaiInstanceApi(credentials)

asyncio.run(api.document().list_documents())
```

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
