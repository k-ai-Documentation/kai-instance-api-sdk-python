import httpx


class SemanticGraph:
    """
    A class to interact with a semantic graph API, providing methods to retrieve nodes,
    linked nodes, nodes by label, and detect approximate nodes.
    """

    def __init__(self, headers, base_url):
        """
        Initializes the SemanticGraph client.

        :param headers: HTTP headers to include in requests.
        :param base_url: The base URL for the API.
        """
        self.__baseurl = base_url
        self.__headers = headers

    async def get_nodes(self, limit, offset):
        """
        Retrieves a paginated list of nodes from the semantic graph.

        :param limit: The maximum number of nodes to retrieve. Maximum is 50, by default is 20.
        :param offset: The starting point for pagination.
        :return: The response containing nodes data or an error message.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/semantic-graph/nodes", headers=self.__headers,
                                             json={
                                                 "limit": limit if not limit else 20,
                                                 "offset": offset if not offset else 0,
                                             })
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_linked_nodes(self, id):
        """
        Retrieves nodes that are linked to a given node ID.

        :param id: The ID of the node whose linked nodes are to be retrieved.
        :return: The response containing linked nodes data or an error message.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/semantic-graph/linked-nodes", headers=self.__headers,
                                             json={
                                                 "id": id
                                             })
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_node_by_label(self, label):
        """
        Retrieves nodes that match a specific label.

        :param label: The label of the node to retrieve.
        :return: The response containing nodes matching the label or an error message.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/semantic-graph/nodes-by-label",
                                             headers=self.__headers,
                                             json={
                                                 "label": label
                                             })
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def detect_approximate_nodes(self, query, need_documents_content):
        """
        Detects and retrieves nodes that approximately match a given query.

        :param need_documents_content: whether response contains content
        :param query: The search query used to identify nodes.
        :return: The response containing detected nodes or an error message.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/semantic-graph/identify-nodes",
                                             headers=self.__headers,
                                             json={
                                                 "query": query,
                                                 "need_documents_content": need_documents_content
                                             })
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
