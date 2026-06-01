# Design: Python SDK Parity with JS SDK

**Date:** 2026-06-01  
**Scope:** Full rewrite of `kai-instance-api-sdk-python` to match `kai-instance-api-sdk-js` exactly. Breaking change. Python 3.12+.

---

## Goal

Bring the Python SDK to feature and structural parity with the JavaScript SDK. The JS SDK is the source of truth.

---

## File Structure

```
kai_sdk_python/
  __init__.py
  index.py                  # KaiInstanceApi, KaiStudioCredentials, State, RetryOptions
  modules/
    __init__.py
    http_client.py          # HttpClient (retry, timeout, response unwrapping)
    base_module.py          # BaseModule (abstract, delegates to HttpClient)
    document.py             # Document module
    orchestrator.py         # Orchestrator module
    semantic_graph.py       # SemanticGraph module
    km_audit.py             # KMAudit module

example.py                  # Updated to use KaiInstanceApi
setup.py                    # Version bump to 20260601
CLAUDE.md                   # Updated to reflect actual structure
```

**Deleted files:** `modules/Core.py`, `modules/KaiStudioCredentials.py`

---

## Credentials & Entry Point (`index.py`)

### `KaiStudioCredentials` dataclass

```python
@dataclass
class KaiStudioCredentials:
    api_key: str = ""
    instance_id: str = ""
    host: str = ""
    authorization: str = ""
    api_host: str = ""
```

`organizationId` is dropped. Headers are built by checking each field and only adding non-empty ones:
- `api_key` → `api-key`
- `instance_id` → `instance-id`
- `authorization` → `Authorization`
- `api_host` → `api-host`

### `RetryOptions` dataclass

```python
@dataclass
class RetryOptions:
    max_retries: int = 3
    retry_delay: float = 1.0   # seconds (base, doubled per attempt)
    timeout: float = 30.0      # seconds
```

### `State` enum

```python
class State(str, Enum):
    PARSING_ERROR = "PARSING_ERROR"
    INITIAL_SAVED = "INITIAL_SAVED"
    UPDATED = "UPDATED"
    ON_CONTENT_EXTRACT = "ON_CONTENT_EXTRACT"
    CONTENT_EXTRACTED = "CONTENT_EXTRACTED"
    ON_INDEXATION = "ON_INDEXATION"
    INDEXED = "INDEXED"
```

### `KaiInstanceApi` factory

```python
class KaiInstanceApi:
    def __init__(self, credentials: KaiStudioCredentials, retry_options: RetryOptions | None = None)
    def document(self) -> Document
    def orchestrator(self) -> Orchestrator
    def semantic_graph(self) -> SemanticGraph
    def audit_instance(self) -> KMAudit
    def get_credentials(self) -> KaiStudioCredentials
```

Base URL: `credentials.host` if set, otherwise `https://api.kai-studio.ai/`.

---

## Infrastructure

### `HttpClient` (`modules/http_client.py`)

Wraps `httpx.AsyncClient`. All requests go through `_with_retry()`.

- **Retry conditions:** HTTP 502, 503, 504, or `httpx.RequestError` (network errors)
- **Non-retryable:** all other status codes (4xx, 500, etc.) — raise immediately
- **Backoff:** `retry_delay * 2^attempt` (0s, 1s, 2s, 4s… for attempts 0..max_retries)
- **Response unwrapping:** `response.json()["response"]` for all standard calls
- **Download:** returns raw `bytes` from `response.content` (no unwrapping)
- **SSL:** `verify=False` (matches existing SDK)

```python
class HttpClient:
    RETRYABLE_STATUSES = {502, 503, 504}

    def __init__(self, headers: dict, base_url: str, retry_options: RetryOptions | None = None)
    async def post(self, endpoint: str, data: dict | None = None) -> Any
    async def download(self, endpoint: str, data: dict | None = None) -> bytes
```

### `BaseModule` (`modules/base_module.py`)

Abstract base. Holds an `HttpClient`. All module subclasses inherit from this.

```python
class BaseModule:
    def __init__(self, headers: dict, base_url: str, retry_options: RetryOptions | None = None)
    async def _post(self, endpoint: str, data: dict | None = None) -> Any
    async def _download(self, endpoint: str, data: dict | None = None) -> bytes
```

---

## Module: `Document` (`modules/document.py`)

TypedDicts:

```python
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
```

Methods:

| Method | Endpoint | Payload | Return |
|--------|----------|---------|--------|
| `list_documents(offset=0, limit=20, state=None)` | `api/document/list-docs` | `{offset, limit, state}` | `list[DocumentSignature]` |
| `get_document_detail(id)` | `api/document/doc` | `{id}` | `DocumentSignature \| None` |
| `count_documents(state=None, document_ids=None)` | `api/document/count-documents` | `{state?, document_ids?}` | `int` |
| `download_file(document_id)` | `api/document/download` | `{id}` | `bytes` |
| `docs_by_ids(ids, offset=0, limit=20)` | `api/document/docs-by-ids` | `{ids, offset, limit}` | `list[DocumentSignature]` |

---

## Module: `Orchestrator` (`modules/orchestrator.py`)

No TypedDicts needed.

| Method | Endpoint | Payload | Return |
|--------|----------|---------|--------|
| `launch_partial_indexation()` | `api/orchestrator/differential-indexation` | `{}` | `bool` |
| `reindex_document(document_id)` | `api/orchestrator/reindex-document` | `{id}` | `bool` |
| `retry_index_error_parsing_documents()` | `api/orchestrator/retry-documents-parsing-error` | `{}` | `bool` |
| `count_registered_background_tasks()` | `api/orchestrator/count-back-tasks` | `{}` | `dict[str, int]` |
| `count_registered_background_tasks_for_doc(document_id)` | `api/orchestrator/count-tasks-for-doc` | `{id}` | `dict[str, int]` |

---

## Module: `SemanticGraph` (`modules/semantic_graph.py`)

TypedDicts:

```python
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
```

Methods:

| Method | Endpoint | Payload | Return |
|--------|----------|---------|--------|
| `get_nodes(limit=20, offset=0)` | `api/semantic-graph/nodes` | `{limit, offset}` | `list[SemanticNode]` |
| `get_node_by_label(label)` | `api/semantic-graph/nodes-by-label` | `{label}` | `list[SemanticNode]` |
| `identify_nodes(query, need_documents_content=False)` | `api/semantic-graph/identify-nodes` | `{query, need_documents_content}` | `list[IdentifiedNode]` |
| `linked_nodes_by_id(id)` | `api/semantic-graph/linked-nodes-by-id` | `{id}` | `list[SemanticNode]` |

---

## Module: `KMAudit` (`modules/km_audit.py`)

Enums:

```python
class AnomalyState(str, Enum):
    MANAGED = "managed"
    IGNORED = "ignored"
    DETECTED = "detected"
    REDETECTED = "redetected"
    DISAPPEARED = "disappeared"
```

TypedDicts:

```python
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
```

Methods:

| Method | Endpoint | Return |
|--------|----------|--------|
| `update_conflict_state(id, state)` | `api/audit/conflict-information/set-state` | `bool` |
| `count_conflicts()` | `api/audit/count-conflict-information` | `int` |
| `list_conflicts(limit=200, offset=0, query=None, document_name=None, state=None)` | `api/audit/conflict-information` | `list[Anomaly]` |
| `count_anomalies_per_document(limit=20, offset=0, document_ids=None)` | `api/audit/document-ids-to-manage` | `dict[str, dict[str, int]]` |
| `get_anomalies_for_document(document_id)` | `api/audit/get-anomalies-for-document` | `DocumentAnomalies` |
| `count_conflicts_for_period(begin_date, end_date, state=None)` | `api/audit/count-conflict-by-date` | `dict[str, dict[str, int]]` |
| `count_conflicts_by_state(state)` | `api/audit/count-conflicts-by-state` | `int` |
| `get_conflict_document_pairs(limit=200, offset=0, document_name=None, state=None, sort_order=None)` | `api/audit/get-conflict-document-pair` | `list[ConflictDocumentPair]` |
| `get_conflicts_by_document_pair(document_ids, limit=200, offset=0, state=None)` | `api/audit/get-conflicts-by-document-id-pair` | `list[Anomaly]` |
| `count_conflicts_per_subject(document_ids=None)` | `api/audit/count-conflict-by-subject` | `list[AnomalyTypeNumber]` |
| `get_conflicts_by_subject(subject=None, offset=0, limit=50)` | `api/audit/get-conflict-information-by-subject` | `list[Anomaly]` |
| `check_if_document_is_audited(document_id)` | `api/audit/document-is-analyzed` | `bool` |
| `count_conflicts_by_document_id(document_ids, state=None)` | `api/audit/count-conflict-by-document-ids` | `int` |

Note: `count_conflicts_per_subject` and `count_conflicts_by_document_id` parse string counts from the API into `int` (matches JS SDK behavior).

---

## Supporting Updates

### `example.py`

Rewritten to demonstrate all four modules using `KaiInstanceApi`. Mirrors the JS `example.ts` pattern.

### `setup.py`

- Version: `20260601`
- `python_requires`: `>=3.12`
- Dependencies: `httpx==0.28.0` (unchanged; `aiohttp` removed)

### `CLAUDE.md`

Updated to reflect the actual new structure: `KaiInstanceApi`, four modules, `RetryOptions`, credential fields, etc.

---

## Constraints

- `aiohttp` dependency removed entirely — all HTTP via `httpx`
- `asyncio.gather` in the old `Core.py` is replaced by the simpler per-call pattern (the JS SDK does not batch calls internally)
- No `organizationId` / `organization-id` header
- SSL verification disabled (`verify=False`) throughout
- Python 3.12+ (native union types `X | Y`, no `Optional`)
