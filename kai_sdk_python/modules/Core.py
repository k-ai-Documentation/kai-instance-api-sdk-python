import httpx


class Core:
    """
    Core client for interacting with the orchestrator API.
    """

    def __init__(self, headers: dict, base_url: str):
        """
        Initialize the Core instance.

        :param headers: HTTP headers for API requests.
        :param base_url: Base URL of the orchestrator API.
        """
        self.__baseurl = base_url
        self.__headers = headers

    async def count_documents(self) -> int:
        """
        Count the total number of documents.

        :return: The total number of documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/stats/count-documents",
                    headers=self.__headers
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def count_indexable_documents(self) -> int:
        """
        Count the number of documents that can be indexed.

        :return: The number of indexable documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/stats/count-indexable-documents",
                    headers=self.__headers
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def count_indexed_documents(self) -> int:
        """
        Count the number of documents that have been indexed.

        :return: The number of indexed documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/stats/count-indexed-documents",
                    headers=self.__headers
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def list_docs(self, limit: int, offset: int) -> list:
        """
        Retrieve a list of documents.

        :param limit: Number of documents to return.
        :param offset: Number of documents to skip.
        :return: A list of documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/list-docs",
                    headers=self.__headers,
                    json={"limit": limit, "offset": offset}
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def count_detected_documents(self) -> int:
        """
        Count the number of detected documents.

        :return: The number of detected documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/stats/count-detected-documents",
                    headers=self.__headers
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
    
    async def count_in_progress_indexation_documents(self) -> int:
        """
        Count the number of documents that are currently being indexed.

        :return: The number of documents that are currently being indexed.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/stats/count-inprogress-indexation-documents",
                    headers=self.__headers
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def download_file(self, file_id: str):
        """
        Download a file by its ID.

        :param file_id: The ID of the file to download.
        :return: File details.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/files/download",
                    headers=self.__headers,
                    json={"id": file_id}
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def differential_indexation(self):
        """
        Perform a differential indexation. It will index all new and modified documents.

        :return: Indexation status.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/differential-indexation",
                    headers=self.__headers
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def last_indexation_begin_time(self) -> str:
        """
        Get the start time of the last indexation.

        :return: The start time of the last indexation as a string.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/last-indexation",
                    headers=self.__headers
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def last_indexation_end_time(self) -> str:
        """
        Get the end time of the last finished indexation.

        :return: The end time of the last finished indexation as a string.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/last-finished-indexation",
                    headers=self.__headers
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def list_indexed_documents(self, limit: int, offset: int) -> list:
        """
        Retrieve a list of indexed documents.

        :param limit: Number of indexed documents to return.
        :param offset: Number of indexed documents to skip.
        :return: A list of indexed documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/list-indexed-documents",
                    headers=self.__headers,
                    json={"limit": limit, "offset": offset}
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
