from .base_module import BaseModule


class Orchestrator(BaseModule):
    async def launch_partial_indexation(self) -> bool:
        return await self._post("api/orchestrator/differential-indexation", {})

    async def reindex_document(self, document_id: str) -> bool:
        return await self._post("api/orchestrator/reindex-document", {"id": document_id})

    async def retry_index_error_parsing_documents(self) -> bool:
        return await self._post("api/orchestrator/retry-documents-parsing-error", {})

    async def count_registered_background_tasks(self) -> dict[str, int]:
        return await self._post("api/orchestrator/count-back-tasks", {})

    async def count_registered_background_tasks_for_doc(self, document_id: str) -> dict[str, int]:
        return await self._post("api/orchestrator/count-tasks-for-doc", {"id": document_id})
