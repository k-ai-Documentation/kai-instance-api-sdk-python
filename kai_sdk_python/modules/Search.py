from typing import List, Literal, TypedDict, Dict

import httpx


class DocumentResult:
    """
    Represents a document returned in search results.
    """
    def __init__(self, id: str, name: str, url: str, rate: float):
        self.id = id
        self.name = name
        self.url = url
        self.rate = rate


class SearchLog:
    """
    Represents a log entry for a search request.
    """
    def __init__(self, id: int, query: str, answer_text: str, user_id: str):
        self.id = id
        self.query = query
        self.answer_text = answer_text
        self.user_id = user_id


class ConversationMessage(TypedDict):
    """
    Represents a message in a conversation.
    """
    from_: Literal['user', 'assistant']
    message: str


class SearchResult:
    """
    Represents the result of a search query.
    """
    def __init__(self, query: str, answer: str, confidentRate: float, gotAnswer: bool, reason: str,
                 documents: List[DocumentResult], followingQuestions: List[str]):
        self.query = query
        self.answer = answer
        self.rate = confidentRate
        self.reason = reason
        self.gotAnswer = gotAnswer
        self.documents = documents
        self.followingQuestions = followingQuestions


class Search:
    """
    Provides search-related functionalities via API requests.
    """
    def __init__(self, headers, base_url):
        """
        Initializes the Search instance.
        :param headers: Authentication headers.
        :param base_url: Base URL for the API.
        """
        self.__baseurl = base_url
        self.__headers = headers

    async def query(self, query: str, user: str, impersonate: bool, multiDocuments: bool, needFollowingQuestions: bool) -> SearchResult:
        """
        Executes a search query.
        :param query: The search query string.
        :param user: The userid performing the query.
        :param impersonate: Whether to impersonate another user, by defaut is 'knowledge manager' if is not specified.
        :param multiDocuments: Whether to allow to search in multiple documents.
        :param needFollowingQuestions: Whether to include follow-up questions.
        :return: SearchResult object.
        """
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

    async def get_doc_signature(self, docId: str):
        """
        Retrieves the signature of a specific document.
        :param docId: Document ID.
        :return: Document signature response.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/doc", headers=self.__headers, json={
                    "id": docId
                })
                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def get_doc_ids(self, docIds: List[str]):
        """
        Retrieves details of multiple documents by their IDs.
        :param docIds: List of document IDs.
        :return: Document details response.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/docs", headers=self.__headers, json={
                    "docsIds": docIds
                })
                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def count_done_requests(self) -> int:
        """
        Counts the number of completed search requests.
        :return: The count of completed search requests.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/stats/count-search", headers=self.__headers)
                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def count_answered_done_requests(self) -> int:
        """
        Counts the number of completed search requests with answers.
        :return: The count of answered search requests.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/stats/count-answered-search",
                                             headers=self.__headers)
                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def get_requests_to_api(self, limit: int, offset: int) -> List[SearchLog]:
        """
        Retrieves a list of search requests made to the API.
        :param limit: Maximum number of records to retrieve.
        :param offset: Offset for pagination.
        :return: List of SearchLog objects.
        """
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
        """
        Identifies a specific question based on a conversation.
        :param conversation: List of conversation messages like [{ from: 'user' | 'assistant', message: string }].
        :return: Response dictionary containing founded correct question or ai will ask you to clarify.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/search/identify-specific-document",
                                             headers=self.__headers,
                                             json={"conversation": conversation})
                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)
