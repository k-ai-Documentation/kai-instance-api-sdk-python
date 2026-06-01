import asyncio

from kai_sdk_python import KaiInstanceApi, KaiStudioCredentials, RetryOptions, State, AnomalyState

credentials = KaiStudioCredentials(
    api_key="your-api-key",
    instance_id="your-instance-id",
)

# Optional: configure retry and timeout behavior
retry_options = RetryOptions(max_retries=3, retry_delay=1.0, timeout=30.0)

api = KaiInstanceApi(credentials, retry_options)


async def demo_document():
    doc = api.document()

    print("LIST DOCUMENTS")
    print(await doc.list_documents(offset=0, limit=5))

    print("COUNT ALL DOCUMENTS")
    print(await doc.count_documents())

    print("COUNT INDEXED DOCUMENTS")
    print(await doc.count_documents(state=State.INDEXED))

    print("COUNT DOCUMENTS BY IDS")
    print(await doc.count_documents(document_ids=["doc-id-1", "doc-id-2"]))

    print("GET DOCUMENT DETAIL")
    print(await doc.get_document_detail("your-document-id"))

    print("DOCS BY IDS")
    print(await doc.docs_by_ids(["doc-id-1", "doc-id-2"]))

    print("DOWNLOAD FILE")
    data = await doc.download_file("your-document-id")
    print(f"Downloaded {len(data)} bytes")


async def demo_orchestrator():
    orch = api.orchestrator()

    print("LAUNCH PARTIAL INDEXATION")
    print(await orch.launch_partial_indexation())

    print("REINDEX DOCUMENT")
    print(await orch.reindex_document("your-document-id"))

    print("RETRY PARSING ERRORS")
    print(await orch.retry_index_error_parsing_documents())

    print("COUNT BACKGROUND TASKS")
    print(await orch.count_registered_background_tasks())

    print("COUNT BACKGROUND TASKS FOR DOC")
    print(await orch.count_registered_background_tasks_for_doc("your-document-id"))


async def demo_semantic_graph():
    sg = api.semantic_graph()

    print("GET NODES")
    print(await sg.get_nodes(limit=10, offset=0))

    print("GET NODE BY LABEL")
    print(await sg.get_node_by_label("Python"))

    print("IDENTIFY NODES")
    print(await sg.identify_nodes("what is machine learning?"))

    print("IDENTIFY NODES WITH CONTENT")
    print(await sg.identify_nodes("what is machine learning?", need_documents_content=True))

    print("LINKED NODES BY ID")
    print(await sg.linked_nodes_by_id("your-node-id"))


async def demo_audit():
    audit = api.audit_instance()

    print("COUNT CONFLICTS")
    print(await audit.count_conflicts())

    print("LIST CONFLICTS")
    print(await audit.list_conflicts(limit=10))

    print("LIST CONFLICTS WITH FILTERS")
    print(await audit.list_conflicts(query="python", state=AnomalyState.DETECTED))

    print("UPDATE CONFLICT STATE")
    print(await audit.update_conflict_state("anomaly-id", AnomalyState.MANAGED))

    print("COUNT ANOMALIES PER DOCUMENT")
    print(await audit.count_anomalies_per_document(limit=10))

    print("GET ANOMALIES FOR DOCUMENT")
    print(await audit.get_anomalies_for_document("your-document-id"))

    print("COUNT CONFLICTS FOR PERIOD")
    print(await audit.count_conflicts_for_period("2026-01-01", "2026-06-01"))

    print("COUNT CONFLICTS BY STATE")
    print(await audit.count_conflicts_by_state(AnomalyState.DETECTED))

    print("GET CONFLICT DOCUMENT PAIRS")
    print(await audit.get_conflict_document_pairs(limit=10))

    print("GET CONFLICTS BY DOCUMENT PAIR")
    print(await audit.get_conflicts_by_document_pair(["doc-id-1", "doc-id-2"]))

    print("COUNT CONFLICTS PER SUBJECT")
    print(await audit.count_conflicts_per_subject())

    print("GET CONFLICTS BY SUBJECT")
    print(await audit.get_conflicts_by_subject(subject="machine learning"))

    print("CHECK IF DOCUMENT IS AUDITED")
    print(await audit.check_if_document_is_audited("your-document-id"))

    print("COUNT CONFLICTS BY DOCUMENT ID")
    print(await audit.count_conflicts_by_document_id(["doc-id-1", "doc-id-2"]))


if __name__ == "__main__":
    asyncio.run(demo_document())
    asyncio.run(demo_orchestrator())
    asyncio.run(demo_semantic_graph())
    asyncio.run(demo_audit())
