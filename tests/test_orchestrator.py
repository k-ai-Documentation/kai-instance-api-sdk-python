from unittest.mock import AsyncMock

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
