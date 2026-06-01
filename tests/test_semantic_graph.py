from unittest.mock import AsyncMock

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
