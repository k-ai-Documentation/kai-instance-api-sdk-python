import httpx


class SemanticGraph:

    def __init__(self, headers, base_url):
        self.__baseurl = base_url
        self.__headers = headers

    async def get_nodes(self, limit, offset):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/semantic-graph/nodes", headers=self.__headers,
                                             json={
                                                 "limit": limit if not limit else 20,
                                                 "offset": offset if not offset else 0,
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_linked_nodes(self, id):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/semantic-graph/linked-nodes", headers=self.__headers,
                                             json={
                                                 "id": id
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_node_by_label(self, label):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/semantic-graph/nodes-by-label",
                                             headers=self.__headers,
                                             json={
                                                 "label": label
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def detect_approximate_nodes(self, query):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/semantic-graph/identify-nodes",
                                             headers=self.__headers,
                                             json={
                                                 "query": query
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
