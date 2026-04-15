# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

The only runtime dependency is `httpx==0.28.0`. Python 3.8+ is required.

## Running Examples

There is no test suite. Behavior is validated through example scripts:

```bash
python example.py       # Full module demonstrations
python chat-example.py  # Chatbot-specific example
```

To test a single module manually:

```python
import asyncio
from kai_sdk_python.index import KaiStudio, KaiStudioCredentials

credentials = KaiStudioCredentials(apiKey="...", organizationId="...", instanceId="...")
search = KaiStudio(credentials).search()

asyncio.run(search.query("test query", "user123", False, False, False))
```

## Architecture

The SDK is a Python async client for the **KAI Studio** platform — an enterprise semantic search and knowledge management system.

### Entry Point

`KaiStudio` (`kai_sdk_python/index.py`) is a factory class. Instantiate it with `KaiStudioCredentials`, then call getter methods to access modules:

```python
studio = KaiStudio(credentials)
studio.search()          # Search
studio.core()            # Document management
studio.km_audit()        # Knowledge management auditing
studio.semantic_graph()  # Graph queries
studio.manage_instance() # Instance/API management
studio.chatbot()         # Conversational interface
studio.file_instance()   # File upload/download
```

### Credentials & Base URLs

Two deployment modes, both use `KaiStudioCredentials`:

- **SaaS**: Requires `organizationId`, `instanceId`, and `apiKey`. Sends `api-key`, `organization-id`, `instance-id` headers. Base URL: `https://api.kai-studio.ai/`
- **Premise**: Only `apiKey` (optional) + `host`. Sends only `api-key` header. Base URL: the custom host.

`FileInstance` always uses a separate endpoint: `https://fma.kai-studio.ai/` (or `{host}/fma/`).

### Modules

| Module | File | Responsibility |
|--------|------|----------------|
| `Core` | `modules/Core.py` | Document lifecycle, indexation, state queries |
| `Search` | `modules/Search.py` | Semantic search, logs, statistics |
| `KMAudit` | `modules/KMAudit.py` | Conflict/duplicate detection, missing subjects |
| `SemanticGraph` | `modules/SemanticGraph.py` | Graph node queries and traversal |
| `ManageInstance` | `modules/ManageInstance.py` | API key management, instance deploy/delete, knowledge bases |
| `Chatbot` | `modules/Chatbot.py` | Conversation history, message sending |
| `FileInstance` | `modules/FileInstance.py` | File upload/download/delete via FMA API |

### Document State Machine

Documents progress through these states (defined as string constants used in `Core` queries):

```
TYPE_ERROR → INITIAL_SAVED → UPDATED → ON_CONTENT_EXTRACT
          → CONTENT_EXTRACTED → ON_INDEXATION → INDEXED
```

### Async Pattern

All API methods are `async def` using `httpx.AsyncClient`. `Core.py` additionally uses `aiohttp` for concurrent batch requests via `asyncio.gather()`. All callers must use `asyncio.run()` or an existing event loop.

### Response Handling

All modules follow the same pattern:
- Success: return `response.json()['response']`
- Error: print exception to stdout, return empty list / `0` / `None` (graceful degradation)

SSL verification is disabled (`verify=False`) across all HTTP calls. There are no request timeouts.

### TypedDict Data Models

Key types defined in `kai_sdk_python/modules/`:
- `DocumentResult`, `SearchResult`, `SearchLog` — search-related
- `ConversationMessage` — chat messages (`role: "user" | "assistant"`)
- `KaiStudioFileSignature`, `KaiStudioFileUploadResponse` — file metadata