from typing import List

import httpx


class KaiStudioFileSignature:
    name: str
    metadata: str

    def __init__(self, name: str, metadata: str, lastModified: str, size: int):
        self.name = name
        self.metadata = metadata
        self.lastModified = lastModified
        self.size = size


class KaiStudioFileUploadResponse:
    result: bool
    reason: str

    def __init__(self, result: bool, reason: str):
        self.result = result
        self.reason = reason


class FileInstance:

    def __init__(self, headers):
        self.__headers = headers
        self.__baseurl = "https://fma.kai-studio.ai/"

    async def list_files(self) -> List[KaiStudioFileSignature]:
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "list-files", headers=self.__headers)
                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def upload_files(self, files) -> List[KaiStudioFileUploadResponse]:
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                if len(files) == 0:
                    return []

                response = await client.post(self.__baseurl + "upload-file", files=files, headers=self.__headers)
                return response.json()["response"] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def delete_files(self, fileName: str) -> bool:
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "delete-file", headers=self.__headers, json={
                    "file": fileName
                })

                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)

    async def download_file(self, fileName: str) :
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "download-file", headers=self.__headers, json={
                    "fileName": fileName
                })

                return response.json()['response'] if response.status_code == 200 else response.text

            except Exception as err:
                print(err)