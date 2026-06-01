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
    async def update_conflict_state(self, id: str, state: AnomalyState) -> bool:
        return await self._post("api/audit/conflict-information/set-state", {"id": id, "state": state})

    async def count_conflicts(self) -> int:
        return await self._post("api/audit/count-conflict-information", {})

    async def list_conflicts(
        self,
        limit: int = 200,
        offset: int = 0,
        query: str | None = None,
        document_name: str | None = None,
        state: AnomalyState | None = None,
    ) -> list[Anomaly]:
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
        return await self._post(
            "api/audit/document-ids-to-manage",
            {"limit": limit, "offset": offset, "document_ids": document_ids},
        )

    async def get_anomalies_for_document(self, document_id: str) -> DocumentAnomalies:
        return await self._post("api/audit/get-anomalies-for-document", {"id": document_id})

    async def count_conflicts_for_period(
        self,
        begin_date: str,
        end_date: str,
        state: AnomalyState | None = None,
    ) -> dict[str, dict[str, int]]:
        return await self._post(
            "api/audit/count-conflict-by-date",
            {"begin_date": begin_date, "end_date": end_date, "state": state},
        )

    async def count_conflicts_by_state(self, state: AnomalyState) -> int:
        return await self._post("api/audit/count-conflicts-by-state", {"state": state})

    async def get_conflict_document_pairs(
        self,
        limit: int = 200,
        offset: int = 0,
        document_name: str | None = None,
        state: str | None = None,
        sort_order: str | None = None,
    ) -> list[ConflictDocumentPair]:
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
        payload: dict = {"document_ids": document_ids, "limit": limit, "offset": offset}
        if state is not None:
            payload["state"] = state
        return await self._post("api/audit/get-conflicts-by-document-id-pair", payload)

    async def count_conflicts_per_subject(
        self,
        document_ids: list[str] | None = None,
    ) -> list[AnomalyTypeNumber]:
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
        return await self._post(
            "api/audit/get-conflict-information-by-subject",
            {"subject": subject, "offset": offset, "limit": limit},
        )

    async def check_if_document_is_audited(self, document_id: str) -> bool:
        return await self._post("api/audit/document-is-analyzed", {"id": document_id})

    async def count_conflicts_by_document_id(
        self,
        document_ids: list[str],
        state: AnomalyState | None = None,
    ) -> int:
        raw: str = await self._post(
            "api/audit/count-conflict-by-document-ids",
            {"document_ids": document_ids, "state": state},
        )
        return int(raw)
