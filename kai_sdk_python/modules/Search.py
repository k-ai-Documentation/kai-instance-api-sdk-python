from typing import List, Literal, TypedDict, Dict

import httpx


class DocumentResult:

    def __init__(self, id: str, name: str, url: str, rate: float):
        self.id = id
        self.name = name
        self.url = url
        self.rate = rate


class SearchLog:
    def __init__(self, id: int, query: str, answer_text: str, user_id: str):
        self.id = id
        self.query = query
        self.answer_text = answer_text
        self.user_id = user_id


class ConversationMessage(TypedDict):
    from_: Literal['user', 'assistant']
    message: str


class SearchResult:
    query: str
    answer: str
    confidentRate: float
    gotAnswer: bool
    reason: str
    documents: List[DocumentResult]
    followingQuestions: List[str]

    def __init__(self, query: str, answer: str, confidentRate: float, gotAnswer: bool, reason: str,
                 documents: List[DocumentResult],
                 followingQuestions: List[str]):
        self.query = query
        self.answer = answer
        self.rate = confidentRate
        self.reason = reason
        self.gotAnswer = gotAnswer
        self.documents = documents
        self.followingQuestions = followingQuestions


class Search:

    def __init__(self, headers, base_url):
        self.__baseurl = base_url
        self.__headers = headers

    # return SearchResult
    async def query(self, query, user, impersonate, multiDocuments, needFollowingQuestions) -> SearchResult:
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/query", headers=self.__headers, json={
                    "query": query,
                    "user": user,
                    "impersonate": impersonate,
                    "multiDocuments": multiDocuments,
                    "needFollowingQuestions": needFollowingQuestions
                })
                return response.json()["response"] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def get_doc_signature(self, docId):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/doc", headers=self.__headers, json={
                    "id": docId
                })

                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def get_doc_ids(self, docIds):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/docs", headers=self.__headers, json={
                    "docsIds": docIds
                })

                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def count_done_requests(self) -> int:
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/stats/count-search", headers=self.__headers)

                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def count_answered_done_requests(self) -> int:
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/stats/count-answered-search",
                                             headers=self.__headers)

                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def get_requests_to_api(self, limit, offset) -> List[SearchLog]:
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/stats/list-search", headers=self.__headers,
                                             json={
                                                 "limit": limit,
                                                 "offset": offset
                                             })
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def identify_specific_document(self, conversation: List[ConversationMessage]) -> Dict:
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/identify-specific-document",
                                             headers=self.__headers,
                                             json={"conversation": conversation})
                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)
