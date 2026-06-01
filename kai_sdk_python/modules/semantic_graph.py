from typing import TypedDict

from .base_module import BaseModule


class SemanticNodeExtraproperties(TypedDict):
    documents: list[str]
    chunks: list[str]
    count: int


class SemanticNode(TypedDict):
    id: str
    node_1: str
    node_2: str
    edge: str
    extraproperties: SemanticNodeExtraproperties


class PartialDocument(TypedDict):
    id: str
    content: list[str]


class IdentifiedNode(TypedDict):
    id: str
    node1: str
    node2: str
    edge: str
    documents: list[PartialDocument] | list[str]


class SemanticGraph(BaseModule):
    async def get_nodes(self, limit: int = 20, offset: int = 0) -> list[SemanticNode]:
        return await self._post("api/semantic-graph/nodes", {"limit": limit, "offset": offset})

    async def get_node_by_label(self, label: str) -> list[SemanticNode]:
        return await self._post("api/semantic-graph/nodes-by-label", {"label": label})

    async def identify_nodes(
        self,
        query: str,
        need_documents_content: bool = False,
    ) -> list[IdentifiedNode]:
        return await self._post(
            "api/semantic-graph/identify-nodes",
            {"query": query, "need_documents_content": need_documents_content},
        )

    async def linked_nodes_by_id(self, id: str) -> list[SemanticNode]:
        return await self._post("api/semantic-graph/linked-nodes-by-id", {"id": id})
