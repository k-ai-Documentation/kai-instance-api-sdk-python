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
    """Module for managing KAI Studio documents."""

    async def list_documents(
        self,
        offset: int = 0,
        limit: int = 20,
        state: str | None = None,
    ) -> list[DocumentSignature]:
        """Return a paginated list of documents, optionally filtered by lifecycle state.

        Args:
            offset: Number of documents to skip (for pagination).
            limit: Maximum number of documents to return (default 20).
            state: Filter by :class:`~kai_sdk_python.index.State` value. ``None`` returns all states.

        Returns:
            List of :class:`DocumentSignature` objects.
        """
        return await self._post("api/document/list-docs", {"offset": offset, "limit": limit, "state": state})

    async def get_document_detail(self, id: str) -> DocumentSignature | None:
        """Return full metadata for a single document.

        Args:
            id: The document's unique identifier.

        Returns:
            A :class:`DocumentSignature` if found, otherwise ``None``.
        """
        return await self._post("api/document/doc", {"id": id})

    async def count_documents(
        self,
        state: str | None = None,
        document_ids: list[str] | None = None,
    ) -> int:
        """Return the number of documents matching the given filters.

        Args:
            state: Restrict count to documents in this lifecycle state. ``None`` counts all states.
            document_ids: Restrict count to this explicit set of document IDs.

        Returns:
            Integer count of matching documents.
        """
        payload: dict = {}
        if state is not None:
            payload["state"] = state
        if document_ids is not None:
            payload["document_ids"] = document_ids
        return await self._post("api/document/count-documents", payload)

    async def download_file(self, document_id: str) -> bytes:
        """Download the raw file content of a document.

        Args:
            document_id: The document's unique identifier.

        Returns:
            Raw file bytes.
        """
        return await self._download("api/document/download", {"id": document_id})

    async def docs_by_ids(
        self,
        ids: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[DocumentSignature]:
        """Return a paginated list of documents for a specific set of IDs.

        Args:
            ids: List of document IDs to retrieve.
            offset: Number of results to skip (for pagination).
            limit: Maximum number of results to return (default 20).

        Returns:
            List of :class:`DocumentSignature` objects matching the given IDs.
        """
        return await self._post("api/document/docs-by-ids", {"ids": ids, "offset": offset, "limit": limit})
