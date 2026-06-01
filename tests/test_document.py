from unittest.mock import AsyncMock

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
