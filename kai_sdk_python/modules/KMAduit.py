import httpx


class KMAudit:

    def __init__(self, headers, base_url):
        self.__baseurl = base_url
        self.__headers = headers

    async def get_conflict_information(self, limit, offset):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/audit/conflict-information", headers=self.__headers,
                                             json={
                                                 "limit": limit if not limit else 20,
                                                 "offset": offset if not offset else 0,
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_duplicated_information(self, limit, offset):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/audit/duplicated-information",
                                             headers=self.__headers,
                                             json={
                                                 "limit": limit if not limit else 20,
                                                 "offset": offset if not offset else 0,
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def set_conflict_managed(self, information_id):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/audit/conflict-information/set-managed",
                                             headers=self.__headers,
                                             json={
                                                 "id": information_id
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def set_duplicated_information_managed(self, information_id):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/audit/duplicated-information/set-managed",
                                             headers=self.__headers,
                                             json={
                                                 "id": information_id
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_documents_to_manage(self, limit, offset):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/audit/documents-to-manage", headers=self.__headers,
                                             json={
                                                 "limit": limit if not limit else 20,
                                                 "offset": offset if not offset else 0,
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def get_missing_subjects(self, limit, offset):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/audit/missing-subjects", headers=self.__headers,
                                             json={
                                                 "limit": limit if not limit else 20,
                                                 "offset": offset if not offset else 0,
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
