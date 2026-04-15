# kai-instance-api-sdk-python

## Introduction

SDK python enables developers to manage documents, perform audits, and explore the semantic graph of KAI instances.

## Installation
Install with pip:
```
pip install git+https://github.com/k-ai-Documentation/kai-instance-api-sdk-python.git
```

## Quick start

There are two types of deployment: SaaS and Premise.

#### SaaS version

Requires `organizationId`, `instanceId`, and `apiKey`:

```python
from kai_sdk_python.index import KaiStudioBackApi, KaiStudioCredentials

credentials = KaiStudioCredentials(organizationId="your organization id",
                                   instanceId="your instance id",
                                   apiKey="your api key")

core = KaiStudioBackApi(credentials).core()
print(await core.count_documents())
```

#### Premise version

Requires `host` and optionally `apiKey`:

```python
from kai_sdk_python.index import KaiStudioBackApi, KaiStudioCredentials

credentials = KaiStudioCredentials(host="your server host", apiKey="your api key")
core = KaiStudioBackApi(credentials).core()
print(await core.count_documents())
```

## Usage Guide

### Core

[Core.py](kai_sdk_python/modules/Core.py) provides methods for document and orchestration management.

- `count_documents` — total document count
- `count_indexable_documents` — count of indexable documents
- `count_indexed_documents` — count of indexed documents
- `count_detected_documents` — count of detected documents
- `count_in_progress_indexation_documents` — count of documents currently being indexed
- `count_document_by_state(state)` — count by state; see [Document States](#document-states)
- `download_file(id)` — download a document by id
- `list_docs(limit, offset, state)` — paginated document list, optionally filtered by state
- `differential_indexation` — index only new/updated/removed documents
- `last_indexation_begin_time` — timestamp when last indexation started
- `last_indexation_end_time` — timestamp when last indexation ended
- `check_pending_job` — background jobs currently in progress
- `get_doc_signature(id)` — get a document's signature
- `get_doc_ids(docsIds)` — get signatures for multiple document ids

```python
core = KaiStudioBackApi(credentials).core()
print(await core.count_documents())
print(await core.list_docs(20, 0, 'INDEXED'))
```

### Auditing

[KMAudit.py](kai_sdk_python/modules/KMAudit.py) provides methods for auditing.

- `get_conflict_information(limit, offset)` — list conflict anomalies
- `get_duplicated_information(limit, offset)` — list duplicate anomalies
- `set_conflict_managed(id)` — mark a conflict as managed
- `set_duplicated_information_managed(id)` — mark a duplicate as managed
- `get_documents_to_manage(limit, offset)` — list documents with unresolved anomalies
- `get_missing_subjects(limit, offset)` — list subjects missing from the knowledge base
- `get_anomalies_for_doc(doc_id)` — get conflicts and duplicates for a document
- `count_missing_subjects` — count missing subjects
- `count_duplicated_information` — count duplicate anomalies
- `count_conflict_information` — count conflict anomalies

```python
km_audit = KaiStudioBackApi(credentials).km_audit()
print(await km_audit.get_conflict_information(20, 0))
```

### SemanticGraph

[SemanticGraph.py](kai_sdk_python/modules/SemanticGraph.py) provides methods for exploring the semantic graph.

- `get_nodes(limit, offset)` — list all semantic nodes
- `get_linked_nodes(id)` — get nodes linked to a given node
- `get_node_by_label(label)` — get nodes by label tag
- `detect_approximate_nodes(query, need_documents_content)` — identify nodes relevant to a query

```python
semantic_graph = KaiStudioBackApi(credentials).semantic_graph()
print(await semantic_graph.get_nodes(10, 0))
```

#### Document States

```python
'TYPE_ERROR'          # document type is not supported
'INITIAL_SAVED'       # initial save
'UPDATED'             # document updated without content reparse
'ON_CONTENT_EXTRACT'  # content extraction in progress
'CONTENT_EXTRACTED'   # content extracted and chunks saved
'ON_INDEXATION'       # indexation in progress
'INDEXED'             # fully indexed
```

<u>**For more examples, see [example.py](example.py).**</u>

## Contributing

bxu@k-ai.ai

rmei@k-ai.ai

sngo@k-ai.ai
