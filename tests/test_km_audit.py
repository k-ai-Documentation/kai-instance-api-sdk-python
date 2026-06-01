from unittest.mock import AsyncMock

import pytest

from kai_sdk_python.modules.km_audit import KMAudit, AnomalyState


def make_module():
    return KMAudit({"api-key": "k"}, "https://api.example.com/")


async def test_update_conflict_state():
    m = make_module()
    m._post = AsyncMock(return_value=True)
    result = await m.update_conflict_state("anomaly1", AnomalyState.MANAGED)
    m._post.assert_called_once_with(
        "api/audit/conflict-information/set-state",
        {"id": "anomaly1", "state": AnomalyState.MANAGED}
    )
    assert result is True


async def test_count_conflicts():
    m = make_module()
    m._post = AsyncMock(return_value=15)
    result = await m.count_conflicts()
    m._post.assert_called_once_with("api/audit/count-conflict-information", {})
    assert result == 15


async def test_list_conflicts_defaults():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.list_conflicts()
    m._post.assert_called_once_with(
        "api/audit/conflict-information",
        {"limit": 200, "offset": 0, "query": None, "document_name": None, "state": None}
    )


async def test_list_conflicts_with_filters():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.list_conflicts(limit=50, offset=10, query="python", document_name="guide.pdf", state=AnomalyState.DETECTED)
    m._post.assert_called_once_with(
        "api/audit/conflict-information",
        {"limit": 50, "offset": 10, "query": "python", "document_name": "guide.pdf", "state": AnomalyState.DETECTED}
    )


async def test_count_anomalies_per_document_defaults():
    m = make_module()
    m._post = AsyncMock(return_value={})
    await m.count_anomalies_per_document()
    m._post.assert_called_once_with("api/audit/document-ids-to-manage", {"limit": 20, "offset": 0, "document_ids": None})


async def test_count_anomalies_per_document_with_ids():
    m = make_module()
    m._post = AsyncMock(return_value={})
    await m.count_anomalies_per_document(document_ids=["a", "b"])
    m._post.assert_called_once_with(
        "api/audit/document-ids-to-manage",
        {"limit": 20, "offset": 0, "document_ids": ["a", "b"]}
    )


async def test_get_anomalies_for_document():
    m = make_module()
    m._post = AsyncMock(return_value={"conflicts": []})
    result = await m.get_anomalies_for_document("doc1")
    m._post.assert_called_once_with("api/audit/get-anomalies-for-document", {"id": "doc1"})
    assert result == {"conflicts": []}


async def test_count_conflicts_for_period_no_state():
    m = make_module()
    m._post = AsyncMock(return_value={})
    await m.count_conflicts_for_period("2026-01-01", "2026-01-31")
    m._post.assert_called_once_with(
        "api/audit/count-conflict-by-date",
        {"begin_date": "2026-01-01", "end_date": "2026-01-31", "state": None}
    )


async def test_count_conflicts_by_state():
    m = make_module()
    m._post = AsyncMock(return_value=7)
    result = await m.count_conflicts_by_state(AnomalyState.DETECTED)
    m._post.assert_called_once_with("api/audit/count-conflicts-by-state", {"state": AnomalyState.DETECTED})
    assert result == 7


async def test_get_conflict_document_pairs_defaults():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_conflict_document_pairs()
    m._post.assert_called_once_with(
        "api/audit/get-conflict-document-pair",
        {"limit": 200, "offset": 0, "document_name": None, "state": None, "order": None}
    )


async def test_get_conflicts_by_document_pair_no_state():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_conflicts_by_document_pair(["docA", "docB"])
    m._post.assert_called_once_with(
        "api/audit/get-conflicts-by-document-id-pair",
        {"document_ids": ["docA", "docB"], "limit": 200, "offset": 0}
    )


async def test_get_conflicts_by_document_pair_with_state():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_conflicts_by_document_pair(["docA", "docB"], state=AnomalyState.MANAGED)
    call_args = m._post.call_args
    assert call_args[0][1]["state"] == AnomalyState.MANAGED


async def test_count_conflicts_per_subject_parses_string_counts():
    m = make_module()
    m._post = AsyncMock(return_value=[
        {
            "subject": "topic A",
            "count": "5",
            "count_detected": "2",
            "count_managed": "1",
            "count_ignored": "1",
            "count_redetected": "0",
            "count_disappeared": "1",
        }
    ])
    result = await m.count_conflicts_per_subject()
    assert result[0]["count"] == 5
    assert result[0]["count_detected"] == 2
    assert isinstance(result[0]["count"], int)
    assert isinstance(result[0]["count_disappeared"], int)


async def test_count_conflicts_per_subject_with_document_ids():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.count_conflicts_per_subject(document_ids=["d1"])
    m._post.assert_called_once_with("api/audit/count-conflict-by-subject", {"document_ids": ["d1"]})


async def test_get_conflicts_by_subject_defaults():
    m = make_module()
    m._post = AsyncMock(return_value=[])
    await m.get_conflicts_by_subject()
    m._post.assert_called_once_with(
        "api/audit/get-conflict-information-by-subject",
        {"subject": None, "offset": 0, "limit": 50}
    )


async def test_check_if_document_is_audited():
    m = make_module()
    m._post = AsyncMock(return_value=True)
    result = await m.check_if_document_is_audited("doc1")
    m._post.assert_called_once_with("api/audit/document-is-analyzed", {"id": "doc1"})
    assert result is True


async def test_count_conflicts_by_document_id_parses_string():
    m = make_module()
    m._post = AsyncMock(return_value="12")
    result = await m.count_conflicts_by_document_id(["docA", "docB"])
    m._post.assert_called_once_with(
        "api/audit/count-conflict-by-document-ids",
        {"document_ids": ["docA", "docB"], "state": None}
    )
    assert result == 12
    assert isinstance(result, int)


async def test_count_conflicts_by_document_id_with_state():
    m = make_module()
    m._post = AsyncMock(return_value="3")
    result = await m.count_conflicts_by_document_id(["docA"], state=AnomalyState.MANAGED)
    call_args = m._post.call_args
    assert call_args[0][1]["state"] == AnomalyState.MANAGED
    assert result == 3
