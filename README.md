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

`KaiStudioCredentials` fields (all optional, default `""`). Only non-empty fields are sent as request headers.

| Field | Header sent | Description |
|-------|-------------|-------------|
| `api_key` | `api-key` | API key for the instance |
| `instance_id` | `instance-id` | Target instance identifier |
| `authorization` | `Authorization` | Bearer or custom auth token |
| `api_host` | `api-host` | Routing header for multi-host setups |
| `host` | — | Overrides the base URL (default: `https://api.kai-studio.ai/`) |

## Retry Options

`RetryOptions` controls HTTP retry behaviour. All fields have defaults.

| Field | Default | Description |
|-------|---------|-------------|
| `max_retries` | `3` | Number of additional attempts after the first failure |
| `retry_delay` | `1.0` | Base delay in seconds between retries; doubles on each attempt |
| `timeout` | `30.0` | Per-request timeout in seconds |

Retries are triggered by HTTP 502, 503, 504, and network errors. Non-retryable errors (4xx, 500) are raised immediately.

## Usage Guide

### Document

```python
doc = api.document()
```

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `list_documents` | `offset=0, limit=20, state=None` | `list[DocumentSignature]` | Paginated document list, optionally filtered by lifecycle state |
| `get_document_detail` | `id` | `DocumentSignature \| None` | Full metadata for a single document; `None` if not found |
| `count_documents` | `state=None, document_ids=None` | `int` | Count of documents matching the given filters |
| `download_file` | `document_id` | `bytes` | Raw file content of the document |
| `docs_by_ids` | `ids, offset=0, limit=20` | `list[DocumentSignature]` | Paginated metadata for a specific set of document IDs |

```python
docs  = await doc.list_documents(offset=0, limit=20, state=State.INDEXED)
count = await doc.count_documents(state=State.INDEXED)
data  = await doc.download_file("document-id")
batch = await doc.docs_by_ids(["id-1", "id-2"])
```

### Orchestrator

```python
orch = api.orchestrator()
```

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `launch_partial_indexation` | — | `bool` | Trigger a differential run — only new or updated documents are processed |
| `reindex_document` | `document_id` | `bool` | Force a full re-indexation of a single document |
| `retry_index_error_parsing_documents` | — | `bool` | Re-queue all documents currently in the `PARSING_ERROR` state |
| `count_registered_background_tasks` | — | `dict[str, int]` | Pending task counts grouped by task type |
| `count_registered_background_tasks_for_doc` | `document_id` | `dict[str, int]` | Pending task counts for a specific document, grouped by task type |

```python
await orch.launch_partial_indexation()
await orch.reindex_document("document-id")
tasks = await orch.count_registered_background_tasks()
```

### SemanticGraph

```python
sg = api.semantic_graph()
```

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_nodes` | `limit=20, offset=0` | `list[SemanticNode]` | Paginated list of all nodes in the knowledge graph |
| `get_node_by_label` | `label` | `list[SemanticNode]` | Nodes whose label exactly matches the given string |
| `identify_nodes` | `query, need_documents_content=False` | `list[IdentifiedNode]` | Nodes semantically relevant to a natural-language query; set `need_documents_content=True` to include full source document content |
| `linked_nodes_by_id` | `id` | `list[SemanticNode]` | All nodes directly connected to the specified node |

```python
nodes   = await sg.get_nodes(limit=20)
related = await sg.identify_nodes("what is machine learning?")
linked  = await sg.linked_nodes_by_id("node-id")
```

### KMAudit

```python
audit = api.audit_instance()
```

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `count_conflicts` | — | `int` | Total number of conflict anomalies across all documents and states |
| `list_conflicts` | `limit=200, offset=0, query=None, document_name=None, state=None` | `list[Anomaly]` | Paginated conflicts; filter by free-text `query`, `document_name`, or `state` |
| `update_conflict_state` | `id, state` | `bool` | Update a conflict anomaly to a new `AnomalyState` |
| `get_anomalies_for_document` | `document_id` | `DocumentAnomalies` | All conflict anomalies associated with a specific document |
| `count_anomalies_per_document` | `limit=20, offset=0, document_ids=None` | `dict[str, dict[str, int]]` | Anomaly counts per document, keyed by document ID then state name |
| `count_conflicts_for_period` | `begin_date, end_date, state=None` | `dict[str, dict[str, int]]` | Conflict counts grouped by date (ISO 8601) over a given range |
| `count_conflicts_by_state` | `state` | `int` | Number of conflicts in a specific `AnomalyState` |
| `get_conflict_document_pairs` | `limit=200, offset=0, document_name=None, state=None, sort_order=None` | `list[ConflictDocumentPair]` | Document pairs that share at least one conflict, with aggregated counts |
| `get_conflicts_by_document_pair` | `document_ids, limit=200, offset=0, state=None` | `list[Anomaly]` | Conflicts shared between exactly two documents |
| `count_conflicts_per_subject` | `document_ids=None` | `list[AnomalyTypeNumber]` | Conflict counts broken down by subject topic with per-state breakdown |
| `get_conflicts_by_subject` | `subject=None, offset=0, limit=50` | `list[Anomaly]` | Conflicts filtered by subject topic |
| `check_if_document_is_audited` | `document_id` | `bool` | Whether a document has completed conflict analysis |
| `count_conflicts_by_document_id` | `document_ids, state=None` | `int` | Total conflicts involving any of the specified documents |

```python
from kai_sdk_python import AnomalyState

conflicts = await audit.list_conflicts(limit=50, state=AnomalyState.DETECTED)
await audit.update_conflict_state("anomaly-id", AnomalyState.MANAGED)
pairs = await audit.get_conflict_document_pairs(sort_order="desc")
by_subject = await audit.count_conflicts_per_subject()
```

## Document States

Documents move through a fixed lifecycle. Use `State` values to filter API calls.

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

## Anomaly States

```python
from kai_sdk_python import AnomalyState

AnomalyState.DETECTED      # conflict first identified
AnomalyState.REDETECTED    # conflict found again after prior resolution
AnomalyState.MANAGED       # conflict acknowledged and handled
AnomalyState.IGNORED       # conflict marked as not actionable
AnomalyState.DISAPPEARED   # conflict no longer present in the knowledge base
```

For more examples, see [example.py](example.py).

## Contributing

bxu@k-ai.ai

rmei@k-ai.ai

sngo@k-ai.ai
