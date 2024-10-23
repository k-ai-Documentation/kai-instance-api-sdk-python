import httpx


class Core:

    def __init__(self, headers, base_url):
        self.__baseurl = base_url
        self.__headers = headers

    async def count_documents(self):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/orchestrator/stats/count-documents",
                                             headers=self.__headers)
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def count_indexable_documents(self):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/orchestrator/stats/count-indexable-documents",
                                             headers=self.__headers)
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def count_indexed_documents(self):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/orchestrator/stats/count-indexed-documents",
                                             headers=self.__headers)
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def count_detected_documents(self):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/orchestrator/stats/count-detected-documents",
                                             headers=self.__headers)
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def download_file(self, file_id):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/orchestrator/files/download", headers=self.__headers,
                                             json={
                                                 "id": file_id
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def differential_indexation(self):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/orchestrator/differential-indexation",
                                             headers=self.__headers)
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
