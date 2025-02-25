from typing import List
import httpx


class KaiStudioFileSignature:
    """
    Represents a file signature in Kai Studio.
    """

    def __init__(self, name: str, metadata: str, lastModified: str, size: int):
        """
        Initialize a file signature.

        :param name: The name of the file.
        :param metadata: Metadata associated with the file.
        :param lastModified: The last modified timestamp of the file.
        :param size: The size of the file in bytes.
        """
        self.name = name
        self.metadata = metadata
        self.lastModified = lastModified
        self.size = size


class KaiStudioFileUploadResponse:
    """
    Represents the response from uploading a file to Kai Studio.
    """

    def __init__(self, result: bool, reason: str):
        """
        Initialize a file upload response.

        :param result: Whether the upload was successful.
        :param reason: Reason for success or failure.
        """
        self.result = result
        self.reason = reason


class FileInstance:
    """
    Client for interacting with Kai Studio's file management API.
    """

    def __init__(self, headers: dict):
        """
        Initialize the FileInstance client.

        :param headers: HTTP headers required for API authentication.
        """
        self.__headers = headers
        self.__baseurl = "https://fma.kai-studio.ai/"

    async def list_files(self) -> List[KaiStudioFileSignature]:
        """
        List all files available in Kai Studio.

        :return: A list of KaiStudioFileSignature objects representing the files.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(f"{self.__baseurl}list-files", headers=self.__headers)
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def upload_files(self, files: list) -> List[KaiStudioFileUploadResponse]:
        """
        Upload multiple files to Kai Studio.

        :param files: A list containing file data to be uploaded.
        :return: A list of KaiStudioFileUploadResponse objects indicating the upload results.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                if len(files) == 0:
                    return []

                response = await client.post(f"{self.__baseurl}upload-file", files=files, headers=self.__headers)
                return response.json()["response"] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def delete_files(self, fileName: str) -> bool:
        """
        Delete a file from Kai Studio.

        :param fileName: The name of the file to delete.
        :return: True if the file was deleted successfully, otherwise False.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}delete-file",
                    headers=self.__headers,
                    json={"file": fileName}
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def download_file(self, fileName: str):
        """
        Download a file from Kai Studio.

        :param fileName: The name of the file to download.
        :return: The downloaded file content.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}download-file",
                    headers=self.__headers,
                    json={"fileName": fileName}
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
