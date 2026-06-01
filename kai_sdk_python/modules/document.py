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
    async def list_documents(
        self,
        offset: int = 0,
        limit: int = 20,
        state: str | None = None,
    ) -> list[DocumentSignature]:
        return await self._post("api/document/list-docs", {"offset": offset, "limit": limit, "state": state})

    async def get_document_detail(self, id: str) -> DocumentSignature | None:
        return await self._post("api/document/doc", {"id": id})

    async def count_documents(
        self,
        state: str | None = None,
        document_ids: list[str] | None = None,
    ) -> int:
        payload: dict = {}
        if state is not None:
            payload["state"] = state
        if document_ids is not None:
            payload["document_ids"] = document_ids
        return await self._post("api/document/count-documents", payload)

    async def download_file(self, document_id: str) -> bytes:
        return await self._download("api/document/download", {"id": document_id})

    async def docs_by_ids(
        self,
        ids: list[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[DocumentSignature]:
        return await self._post("api/document/docs-by-ids", {"ids": ids, "offset": offset, "limit": limit})
