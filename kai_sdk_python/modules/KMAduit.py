import httpx


class KMAudit:
    """
    Client for interacting with the audit API to manage conflicts, duplicates, and anomalies in documents.
    """

    def __init__(self, headers: dict, base_url: str):
        """
        Initialize the KMAudit client.

        :param headers: HTTP headers required for API authentication.
        :param base_url: The base URL of the audit API.
        """
        self.__baseurl = base_url
        self.__headers = headers

    async def get_conflict_information(self, limit: int = 20, offset: int = 0):
        """
        Retrieve a list of conflict information records.

        :param limit: The number of records to retrieve (default: 20).
        :param offset: The starting position for retrieval (default: 0).
        :return: A list of conflict information records.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/conflict-information",
                    headers=self.__headers,
                    json={"limit": limit, "offset": offset},
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_duplicated_information(self, limit: int = 20, offset: int = 0):
        """
        Retrieve a list of duplicated information records.

        :param limit: The number of records to retrieve (default: 20).
        :param offset: The starting position for retrieval (default: 0).
        :return: A list of duplicated information records.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/duplicated-information",
                    headers=self.__headers,
                    json={"limit": limit, "offset": offset},
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def set_conflict_managed(self, information_id: str):
        """
        Mark a conflict information record as managed.

        :param information_id: The ID of the conflict information to be marked as managed.
        :return: Confirmation response from the API.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/conflict-information/set-managed",
                    headers=self.__headers,
                    json={"id": information_id},
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def set_duplicated_information_managed(self, information_id: str):
        """
        Mark a duplicated information record as managed.

        :param information_id: The ID of the duplicated information to be marked as managed.
        :return: Confirmation response from the API.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/duplicated-information/set-managed",
                    headers=self.__headers,
                    json={"id": information_id},
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_documents_to_manage(self, limit: int = 20, offset: int = 0):
        """
        Retrieve a list of documents that need to be managed.

        :param limit: The number of records to retrieve (default: 20).
        :param offset: The starting position for retrieval (default: 0).
        :return: A list of documents requiring management.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/documents-to-manage",
                    headers=self.__headers,
                    json={"limit": limit, "offset": offset},
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_missing_subjects(self, limit: int = 20, offset: int = 0):
        """
        Retrieve a list of missing subjects.

        :param limit: The number of records to retrieve (default: 20).
        :param offset: The starting position for retrieval (default: 0).
        :return: A list of missing subjects.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/missing-subjects",
                    headers=self.__headers,
                    json={"limit": limit, "offset": offset},
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def count_missing_subjects(self):
        """
        Count the number of missing subjects.

        :return: The total count of missing subjects.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/count-missing-subjects",
                    headers=self.__headers,
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def count_duplicated_information(self):
        """
        Count the number of duplicated information records.

        :return: The total count of duplicated information.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/count-duplicated-information",
                    headers=self.__headers,
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def count_conflict_information(self):
        """
        Count the number of conflict information records.

        :return: The total count of conflict information.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/count-conflict-information",
                    headers=self.__headers,
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_anomalies_for_doc(self, doc_id: str):
        """
        Retrieve a list of anomalies for a specific document.

        :param doc_id: The ID of the document for which anomalies are to be retrieved.
        :return: A list of anomalies for the specified document.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/audit/get-anomalies-for-document",
                    headers=self.__headers,
                    json={"id": doc_id},
                )
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
