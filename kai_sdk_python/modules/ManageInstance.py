from typing import List
import httpx


class ManageInstance:
    """
    This class is for managing instances via the Kai Studio API.
    This class provides methods to check API health, generate API keys,
    update names, deploy and delete instances, manage knowledge bases, and more.
    """
    
    def __init__(self, headers, base_url):
        """
        Initialize the ManageInstance client.

        :param headers: HTTP headers for authentication.
        :param base_url: The base URL of the API.
        """
        self.__baseurl = base_url
        self.__headers = headers

    async def get_global_health(self):
        """
        Retrieve the global health status of the API.
        
        :return: API health response.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://api.kai-studio.ai/global-health", headers=self.__headers)
                return response.json()['response']
            except Exception as err:
                print(err)

    async def is_api_alive(self):
        """
        Check if the API is alive.
        
        :return: Boolean response indicating API status.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://api.kai-studio.ai/health", headers=self.__headers)
                return response.json()['response']
            except Exception as err:
                print(err)

    async def generate_new_api_key(self):
        """
        Generate a new API key.
        
        :return: New API key as a string.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.get("https://ima.kai-studio.ai/generate-new-apikey", headers=self.__headers)
                return response.json()['response']
            except Exception as err:
                print(err)

    async def update_name(self, name: str):
        """
        Update the instance name.
        
        :param name: The new name for the instance.
        :return: API response confirmation.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/update-name", headers=self.__headers, json={"name": name})
                return response.json()['response']
            except Exception as err:
                print(err)

    async def deploy(self, name: str):
        """
        Deploy an instance.
        
        :param name: The name of the instance to deploy.
        :return: API response confirmation.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/deploy", headers=self.__headers)
                return response.json()['response']
            except Exception as err:
                print(err)

    async def delete(self, name: str):
        """
        Delete an instance.
        
        :param name: The name of the instance to delete.
        :return: API response confirmation.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/delete", headers=self.__headers)
                return response.json()['response']
            except Exception as err:
                print(err)

    async def add_kb(self, kb_type: str, options, search_goal: str):
        """
        Add a knowledge base (KB) to the instance.
        
        :param kb_type: Type of knowledge base.
        :param options: Configuration options for the knowledge base.
        :param search_goal: The search goal associated with the KB.
        :return: API response confirmation.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/add-kb", headers=self.__headers, json={"type": kb_type, "options": options, "searchGoal": search_goal})
                return response.json()['response']
            except Exception as err:
                print(err)

    async def set_playground(self, type_list: List[str]):
        """
        Set playground types for the instance.
        
        :param type_list: A list of playground types.
        :return: API response confirmation.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/set-playground", headers=self.__headers, json={"typeList": type_list})
                return response.json()['response']
            except Exception as err:
                print(err)

    async def update_kb(self, id: str, options, search_goal):
        """
        Update a knowledge base (KB).
        
        :param id: The ID of the knowledge base to update.
        :param options: Updated configuration options.
        :param search_goal: Updated search goal.
        :return: API response confirmation.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/update-kb", headers=self.__headers, json={"id": id, "options": options, "searchGoal": search_goal})
                return response.json()['response']
            except Exception as err:
                print(err)

    async def remove_kb(self, id: str):
        """
        Remove a knowledge base (KB) from the instance.
        
        :param id: The ID of the knowledge base to remove.
        :return: API response confirmation.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/remove-kb", headers=self.__headers, json={"id": id})
                return response.json()['response']
            except Exception as err:
                print(err)

    async def get_version(self) -> str:
        """
        Retrieve the API version.
        
        :return: API version as a string.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "version", headers=self.__headers)
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
