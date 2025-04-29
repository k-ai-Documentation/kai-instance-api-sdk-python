import httpx
from typing import List
import asyncio
import aiohttp

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
        try:
            async with aiohttp.ClientSession(verify=False, timeout=None) as client:
                all_doc_task = client.post(
                    f"{self.base_url}api/core/count-documents-by-state",
                    headers=self.headers,
                    json={'state': ''}
                )
                error_type_task = client.post(
                    f"{self.base_url}api/core/count-documents-by-state",
                    headers=self.headers,
                    json={'state': 'TYPE_ERROR'}
                )

                all_doc_response, error_type_response = await asyncio.gather(all_doc_task, error_type_task)

                all_doc_count = int(await all_doc_response.json())['response']
                error_type_count = int(await error_type_response.json())['response']

                return all_doc_count - error_type_count
        except Exception as e:
            print(e)
            return 0

    async def count_indexable_documents(self) -> int:
        """
        Count the number of documents that can be indexed.

        :return: The number of indexable documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                intial_save = client.post(
                    f"{self.__baseurl}api/core/count-documents-by-state",
                    headers=self.__headers,
                    json={"state": "INITIAL_SAVE"}
                )
                updated = client.post(
                    f"{self.__baseurl}api/core/count-documents-by-state",
                    headers=self.__headers,
                    json={"state": "UPDATED"}
                )
                intial_save_response, updated_response = await asyncio.gather(intial_save, updated)
                return intial_save_response.json()['response'] + updated_response.json()['response']
            except Exception as err:
                print(err)
                return 0

    async def count_indexed_documents(self) -> int:
        """
        Count the number of documents that have been indexed.

        :return: The number of indexed documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/core/count-documents-by-state",
                    headers=self.__headers,
                    json={"state": "INDEXED"}
                )
                return response.json()['response']
            except Exception as err:
                print(err)
                return 0

    async def list_docs(self, limit: int, offset: int, state: str = '') -> list:
        """
        Retrieve a list of documents.

        :param limit: Number of documents to return.
        :param offset: Number of documents to skip.
        :param state: State of the documents to retrieve. If state is not specified, all documents will be retrieved.
        :return: A list of documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/list-docs",
                    headers=self.__headers,
                    json={"limit": limit, "offset": offset, "state": state}
                )
                return response.json()['response']
            except Exception as err:
                print(err)
                return []

    async def count_detected_documents(self) -> int:
        """
        Count the number of detected documents.

        :return: The number of detected documents.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/core/count-documents-by-state",
                    headers=self.__headers,
                    json={"state": ''}
                )
                return response.json()['response'] 
            except Exception as err:
                print(err)
                return 0
    
    async def count_in_progress_indexation_documents(self) -> int:
        """
        Count the number of documents that are currently being indexed.

        :return: The number of documents that are currently being indexed.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                on_content_extract = client.post(
                    f"{self.__baseurl}api/core/count-documents-by-state",
                    headers=self.__headers,
                    json={"state": "ON_CONTENT_EXTRACT"}
                )
                content_extract = client.post(
                    f"{self.__baseurl}api/core/count-documents-by-state",
                    headers=self.__headers,
                    json={"state": "CONTENT_EXTRACT"}
                )
                on_indexation = client.post(
                    f"{self.__baseurl}api/core/count-documents-by-state",
                    headers=self.__headers,
                    json={"state": "ON_INDEXATION"}
                )
                on_indexation_response, content_extract_response, on_content_extract_response = await asyncio.gather(on_content_extract, content_extract, on_indexation)
                return on_indexation_response.json()['response'] + content_extract_response.json()['response'] + on_content_extract_response.json()['response']
            except Exception as err:
                print(err)
                return 0

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

    async def count_document_by_state(self, state: str = '') -> list:
        """
        Get the number of documents by state.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/core/count-documents-by-state",
                    headers=self.__headers,
                    json={"state": state }
                )
                return response.json()['response']
            except Exception as err:
                print(err)
                return 0

    async def check_pending_job(self) -> str:
        """
        Get the information about your instance background jobs in progress.

        Available values :

        "Indexation in progress" , "Partial indexation in progress" , "Recovery indexation in progress" : An indexation of new or updated documents is pending.

        "Loading Audit" : "Audit of the indexed documents is pending."
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/orchestrator/check-pending-job",
                    headers=self.__headers
                )
                return response.json()['response'] if response.status_code == 200 else response.text
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
                response = await client.post(self.__baseurl + "api/orchestrator/doc", headers=self.__headers, json={
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
                response = await client.post(self.__baseurl + "api/orchestrator/docs", headers=self.__headers, json={
                    "docsIds": docIds
                })
                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)



