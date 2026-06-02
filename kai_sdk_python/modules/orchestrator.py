from .base_module import BaseModule


class Orchestrator(BaseModule):
    """Module for triggering indexation pipelines and monitoring background tasks."""

    async def launch_partial_indexation(self) -> bool:
        """Trigger a differential (partial) indexation run for new or updated documents.

        Only documents that have changed since the last indexation are processed.

        Returns:
            ``True`` if the indexation was successfully triggered.
        """
        return await self._post("api/orchestrator/differential-indexation", {})

    async def reindex_document(self, document_id: str) -> bool:
        """Force a full re-indexation of a single document.

        Args:
            document_id: The unique identifier of the document to re-index.

        Returns:
            ``True`` if the re-indexation job was successfully queued.
        """
        return await self._post("api/orchestrator/reindex-document", {"id": document_id})

    async def retry_index_error_parsing_documents(self) -> bool:
        """Retry indexation for all documents currently in the ``PARSING_ERROR`` state.

        Returns:
            ``True`` if the retry jobs were successfully queued.
        """
        return await self._post("api/orchestrator/retry-documents-parsing-error", {})

    async def count_registered_background_tasks(self) -> dict[str, int]:
        """Return the count of pending background tasks grouped by task type.

        Returns:
            A mapping of task-type name to the number of queued tasks.
        """
        return await self._post("api/orchestrator/count-back-tasks", {})

    async def count_registered_background_tasks_for_doc(self, document_id: str) -> dict[str, int]:
        """Return the count of pending background tasks for a specific document.

        Args:
            document_id: The unique identifier of the document to query.

        Returns:
            A mapping of task-type name to the number of queued tasks for that document.
        """
        return await self._post("api/orchestrator/count-tasks-for-doc", {"id": document_id})
