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
    """Module for querying the KAI Studio knowledge-graph."""

    async def get_nodes(self, limit: int = 20, offset: int = 0) -> list[SemanticNode]:
        """Return a paginated list of all semantic nodes in the knowledge graph.

        Args:
            limit: Maximum number of nodes to return (default 20).
            offset: Number of nodes to skip (for pagination).

        Returns:
            List of :class:`SemanticNode` objects.
        """
        return await self._post("api/semantic-graph/nodes", {"limit": limit, "offset": offset})

    async def get_node_by_label(self, label: str) -> list[SemanticNode]:
        """Return all nodes whose label (node_1 or node_2) matches the given string.

        Args:
            label: The node label to search for (exact match).

        Returns:
            List of matching :class:`SemanticNode` objects.
        """
        return await self._post("api/semantic-graph/nodes-by-label", {"label": label})

    async def identify_nodes(
        self,
        query: str,
        need_documents_content: bool = False,
    ) -> list[IdentifiedNode]:
        """Identify knowledge-graph nodes that are semantically relevant to a natural-language query.

        Args:
            query: Natural-language query used to find relevant nodes.
            need_documents_content: When ``True``, each :class:`IdentifiedNode` includes the
                full content of its source documents. Defaults to ``False`` for lighter responses.

        Returns:
            List of :class:`IdentifiedNode` objects ranked by relevance.
        """
        return await self._post(
            "api/semantic-graph/identify-nodes",
            {"query": query, "need_documents_content": need_documents_content},
        )

    async def linked_nodes_by_id(self, id: str) -> list[SemanticNode]:
        """Return all nodes directly connected to the specified node.

        Args:
            id: The unique identifier of the source node.

        Returns:
            List of :class:`SemanticNode` objects linked to the given node.
        """
        return await self._post("api/semantic-graph/linked-nodes-by-id", {"id": id})
