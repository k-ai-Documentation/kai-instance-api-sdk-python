from enum import Enum
from typing import TypedDict

from .base_module import BaseModule


class AnomalyState(str, Enum):
    MANAGED = "managed"
    IGNORED = "ignored"
    DETECTED = "detected"
    REDETECTED = "redetected"
    DISAPPEARED = "disappeared"


class AnomalyInformationDocument(TypedDict):
    doc_id: str
    information_involved: str


class Anomaly(TypedDict):
    id: str
    subject: str
    state: AnomalyState
    documents: list[AnomalyInformationDocument]
    explanation: str


class DocumentAnomalies(TypedDict):
    conflicts: list[Anomaly]


class AnomalyTypeNumber(TypedDict):
    subject: str
    count: int
    count_detected: int
    count_managed: int
    count_ignored: int
    count_redetected: int
    count_disappeared: int


class ConflictDocumentPair(TypedDict):
    document_ids: list[str]
    conflict_count: int
    state: str


class KMAudit(BaseModule):
    """Module for conflict anomaly detection and management in the KAI knowledge base."""

    async def update_conflict_state(self, id: str, state: AnomalyState) -> bool:
        """Update the lifecycle state of a conflict anomaly.

        Args:
            id: Unique identifier of the conflict anomaly to update.
            state: New state to assign (e.g. ``AnomalyState.MANAGED`` or ``AnomalyState.IGNORED``).

        Returns:
            ``True`` if the state was successfully updated.
        """
        return await self._post("api/audit/conflict-information/set-state", {"id": id, "state": state})

    async def count_conflicts(self) -> int:
        """Return the total number of conflict anomalies across all documents and states.

        Returns:
            Integer count of all conflict anomalies.
        """
        return await self._post("api/audit/count-conflict-information", {})

    async def list_conflicts(
        self,
        limit: int = 200,
        offset: int = 0,
        query: str | None = None,
        document_name: str | None = None,
        state: AnomalyState | None = None,
    ) -> list[Anomaly]:
        """Return a paginated, filtered list of conflict anomalies.

        Args:
            limit: Maximum number of results to return (default 200).
            offset: Number of results to skip (for pagination).
            query: Free-text search applied to anomaly subjects and explanations.
            document_name: Filter anomalies to those involving this document name.
            state: Filter anomalies by lifecycle state. ``None`` returns all states.

        Returns:
            List of :class:`Anomaly` objects matching the given filters.
        """
        return await self._post(
            "api/audit/conflict-information",
            {"limit": limit, "offset": offset, "query": query, "document_name": document_name, "state": state},
        )

    async def count_anomalies_per_document(
        self,
        limit: int = 20,
        offset: int = 0,
        document_ids: list[str] | None = None,
    ) -> dict[str, dict[str, int]]:
        """Return anomaly counts grouped by document, optionally restricted to specific document IDs.

        Args:
            limit: Maximum number of documents to include in the result (default 20).
            offset: Number of documents to skip (for pagination).
            document_ids: Restrict results to this set of document IDs. ``None`` includes all documents.

        Returns:
            Mapping of document ID to a nested mapping of state name to count.
        """
        return await self._post(
            "api/audit/document-ids-to-manage",
            {"limit": limit, "offset": offset, "document_ids": document_ids},
        )

    async def get_anomalies_for_document(self, document_id: str) -> DocumentAnomalies:
        """Return all conflict anomalies associated with a specific document.

        Args:
            document_id: Unique identifier of the document to inspect.

        Returns:
            A :class:`DocumentAnomalies` object containing the list of conflicts.
        """
        return await self._post("api/audit/get-anomalies-for-document", {"id": document_id})

    async def count_conflicts_for_period(
        self,
        begin_date: str,
        end_date: str,
        state: AnomalyState | None = None,
    ) -> dict[str, dict[str, int]]:
        """Return conflict counts grouped by date for a given time range.

        Args:
            begin_date: Start of the date range (ISO 8601 string, e.g. ``"2024-01-01"``).
            end_date: End of the date range (ISO 8601 string, e.g. ``"2024-12-31"``).
            state: Filter counts to this anomaly state. ``None`` includes all states.

        Returns:
            Mapping of date string to a nested mapping of state name to count.
        """
        return await self._post(
            "api/audit/count-conflict-by-date",
            {"begin_date": begin_date, "end_date": end_date, "state": state},
        )

    async def count_conflicts_by_state(self, state: AnomalyState) -> int:
        """Return the number of conflict anomalies in a specific state.

        Args:
            state: The anomaly state to count (e.g. ``AnomalyState.DETECTED``).

        Returns:
            Integer count of conflicts in the given state.
        """
        return await self._post("api/audit/count-conflicts-by-state", {"state": state})

    async def get_conflict_document_pairs(
        self,
        limit: int = 200,
        offset: int = 0,
        document_name: str | None = None,
        state: str | None = None,
        sort_order: str | None = None,
    ) -> list[ConflictDocumentPair]:
        """Return pairs of documents that share at least one conflict, with aggregated counts.

        Args:
            limit: Maximum number of pairs to return (default 200).
            offset: Number of pairs to skip (for pagination).
            document_name: Filter pairs to those involving this document name.
            state: Filter pairs by anomaly state string.
            sort_order: Sort direction for the results (e.g. ``"asc"`` or ``"desc"``).

        Returns:
            List of :class:`ConflictDocumentPair` objects.
        """
        return await self._post(
            "api/audit/get-conflict-document-pair",
            {"limit": limit, "offset": offset, "document_name": document_name, "state": state, "order": sort_order},
        )

    async def get_conflicts_by_document_pair(
        self,
        document_ids: list[str],
        limit: int = 200,
        offset: int = 0,
        state: AnomalyState | None = None,
    ) -> list[Anomaly]:
        """Return all conflicts shared between a specific pair of documents.

        Args:
            document_ids: Exactly two document IDs whose shared conflicts to retrieve.
            limit: Maximum number of conflicts to return (default 200).
            offset: Number of conflicts to skip (for pagination).
            state: Filter conflicts by anomaly state. ``None`` returns all states.

        Returns:
            List of :class:`Anomaly` objects shared between the two documents.
        """
        payload: dict = {"document_ids": document_ids, "limit": limit, "offset": offset}
        if state is not None:
            payload["state"] = state
        return await self._post("api/audit/get-conflicts-by-document-id-pair", payload)

    async def count_conflicts_per_subject(
        self,
        document_ids: list[str] | None = None,
    ) -> list[AnomalyTypeNumber]:
        """Return conflict counts broken down by subject topic, optionally scoped to specific documents.

        Args:
            document_ids: Restrict aggregation to this set of document IDs. ``None`` aggregates globally.

        Returns:
            List of :class:`AnomalyTypeNumber` objects, one per unique subject, with per-state counts.
        """
        payload: dict = {}
        if document_ids is not None:
            payload["document_ids"] = document_ids
        raw: list = await self._post("api/audit/count-conflict-by-subject", payload)
        return [
            {
                "subject": item["subject"],
                "count": int(item["count"]),
                "count_detected": int(item["count_detected"]),
                "count_managed": int(item["count_managed"]),
                "count_ignored": int(item["count_ignored"]),
                "count_redetected": int(item["count_redetected"]),
                "count_disappeared": int(item["count_disappeared"]),
            }
            for item in raw
        ]

    async def get_conflicts_by_subject(
        self,
        subject: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> list[Anomaly]:
        """Return conflicts filtered by subject topic.

        Args:
            subject: The subject string to filter on. ``None`` returns conflicts across all subjects.
            offset: Number of results to skip (for pagination).
            limit: Maximum number of results to return (default 50).

        Returns:
            List of :class:`Anomaly` objects matching the given subject.
        """
        return await self._post(
            "api/audit/get-conflict-information-by-subject",
            {"subject": subject, "offset": offset, "limit": limit},
        )

    async def check_if_document_is_audited(self, document_id: str) -> bool:
        """Check whether a document has been fully analysed for conflicts.

        Args:
            document_id: Unique identifier of the document to check.

        Returns:
            ``True`` if the document has completed audit analysis.
        """
        return await self._post("api/audit/document-is-analyzed", {"id": document_id})

    async def count_conflicts_by_document_id(
        self,
        document_ids: list[str],
        state: AnomalyState | None = None,
    ) -> int:
        """Return the total number of conflicts involving any of the specified documents.

        Args:
            document_ids: List of document IDs to aggregate conflicts for.
            state: Filter by anomaly state. ``None`` counts conflicts in all states.

        Returns:
            Integer count of matching conflicts.
        """
        raw: str = await self._post(
            "api/audit/count-conflict-by-document-ids",
            {"document_ids": document_ids, "state": state},
        )
        return int(raw)
