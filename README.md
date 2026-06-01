# kai-instance-api-sdk-python

## Introduction

Python SDK for managing documents, auditing knowledge, and exploring the semantic graph of KAI Studio instances.

## Installation

```bash
pip install git+https://github.com/k-ai-Documentation/kai-instance-api-sdk-python.git
```

## Quick Start

```python
import asyncio
from kai_sdk_python import KaiInstanceApi, KaiStudioCredentials

credentials = KaiStudioCredentials(
    api_key="your-api-key",
    instance_id="your-instance-id",
)

api = KaiInstanceApi(credentials)

asyncio.run(api.document().list_documents())
```

### On-Premise deployment

```python
credentials = KaiStudioCredentials(
    host="https://your-server.example.com/",
    api_key="your-api-key",  # optional
)

api = KaiInstanceApi(credentials)
```

### Custom retry / timeout

```python
from kai_sdk_python import RetryOptions

api = KaiInstanceApi(
    credentials,
    RetryOptions(max_retries=3, retry_delay=1.0, timeout=30.0),
)
```

## Credentials

`KaiStudioCredentials` fields (all optional, default `""`):

| Field | Header sent |
|-------|-------------|
| `api_key` | `api-key` |
| `instance_id` | `instance-id` |
| `authorization` | `Authorization` |
| `api_host` | `api-host` |
| `host` | overrides base URL (default: `https://api.kai-studio.ai/`) |

Only non-empty fields are sent as request headers.

## Usage Guide

### Document

```python
doc = api.document()
```

| Method | Description |
|--------|-------------|
| `list_documents(offset, limit, state)` | Paginated document list, optionally filtered by state |
| `get_document_detail(id)` | Full metadata for a single document |
| `count_documents(state, document_ids)` | Count documents, optionally filtered |
| `download_file(document_id)` | Download raw file bytes |
| `docs_by_ids(ids, offset, limit)` | Fetch multiple documents by ID |

```python
docs = await doc.list_documents(offset=0, limit=20, state=State.INDEXED)
count = await doc.count_documents(state=State.INDEXED)
data = await doc.download_file("document-id")
```

### Orchestrator

```python
orch = api.orchestrator()
```

| Method | Description |
|--------|-------------|
| `launch_partial_indexation()` | Index only new/updated documents |
| `reindex_document(document_id)` | Force reindex a single document |
| `retry_index_error_parsing_documents()` | Retry all `PARSING_ERROR` documents |
| `count_registered_background_tasks()` | Count all background tasks by type |
| `count_registered_background_tasks_for_doc(document_id)` | Count background tasks for a document |

```python
await orch.launch_partial_indexation()
await orch.reindex_document("document-id")
```

### SemanticGraph

```python
sg = api.semantic_graph()
```

| Method | Description |
|--------|-------------|
| `get_nodes(limit, offset)` | Paginated list of knowledge graph nodes |
| `get_node_by_label(label)` | Find nodes matching a label |
| `identify_nodes(query, need_documents_content)` | Find nodes relevant to a natural language query |
| `linked_nodes_by_id(id)` | Get all nodes directly connected to a node |

```python
nodes = await sg.get_nodes(limit=20)
related = await sg.identify_nodes("what is machine learning?")
```

### KMAudit

```python
audit = api.audit_instance()
```

| Method | Description |
|--------|-------------|
| `count_conflicts()` | Total conflict count |
| `list_conflicts(limit, offset, query, document_name, state)` | Paginated conflicts with filters |
| `update_conflict_state(id, state)` | Update a conflict's state |
| `get_anomalies_for_document(document_id)` | All anomalies for a document |
| `count_anomalies_per_document(limit, offset, document_ids)` | Conflict counts per document |
| `count_conflicts_for_period(begin_date, end_date, state)` | Conflicts over a date range |
| `count_conflicts_by_state(state)` | Count conflicts by state |
| `get_conflict_document_pairs(...)` | Document pairs sharing conflicts |
| `get_conflicts_by_document_pair(document_ids, ...)` | Conflicts between two documents |
| `count_conflicts_per_subject(document_ids)` | Conflict counts grouped by subject |
| `get_conflicts_by_subject(subject, offset, limit)` | Conflicts filtered by subject |
| `check_if_document_is_audited(document_id)` | Whether a document has been audited |
| `count_conflicts_by_document_id(document_ids, state)` | Conflict count for given documents |

```python
from kai_sdk_python import AnomalyState

conflicts = await audit.list_conflicts(limit=50, state=AnomalyState.DETECTED)
await audit.update_conflict_state("anomaly-id", AnomalyState.MANAGED)
```

## Document States

```python
from kai_sdk_python import State

State.PARSING_ERROR       # document type not supported or parse failed
State.INITIAL_SAVED       # saved, not yet processed
State.UPDATED             # metadata updated
State.ON_CONTENT_EXTRACT  # content extraction in progress
State.CONTENT_EXTRACTED   # content extracted and chunked
State.ON_INDEXATION       # indexation in progress
State.INDEXED             # fully indexed and queryable
```

For more examples, see [example.py](example.py).

## Contributing

bxu@k-ai.ai

rmei@k-ai.ai

sngo@k-ai.ai
