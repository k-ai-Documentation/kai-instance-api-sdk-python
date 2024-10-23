from typing import List

import httpx


class ManageInstance:
    def __init__(self, headers, base_url):
        self.__baseurl = base_url
        self.__headers = headers

    async def get_global_health(self):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://api.kai-studio.ai/global-health", headers=self.__headers)
                return response.text
            except Exception as err:
                print(err)

    async def is_api_alive(self):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://api.kai-studio.ai/health", headers=self.__headers)
                return response.text
            except Exception as err:
                print(err)

    async def generate_new_api_key(self):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.get("https://ima.kai-studio.ai/generate-new-apikey", headers=self.__headers)
                return response.text
            except Exception as err:
                print(err)

    async def update_name(self, name: str):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/update-name", headers=self.__headers, json={
                    "name": name
                })
                return response.text
            except Exception as err:
                print(err)

    async def deploy(self, name: str):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/deploy", headers=self.__headers)
                return response.text
            except Exception as err:
                print(err)

    async def delete(self, name: str):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/delete", headers=self.__headers)
                return response.text
            except Exception as err:
                print(err)

    async def add_kb(self, kb_type: str, options, search_goal: str):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/add-kb", headers=self.__headers, json={
                    "type": kb_type, "options": options, "searchGoal": search_goal
                })
                return response.text
            except Exception as err:
                print(err)

    async def set_playground(self, type_list: List[str]):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/set-playground", headers=self.__headers, json={
                    "typeList": type_list
                })
                return response.text
            except Exception as err:
                print(err)

    async def update_kb(self, id: str, options, search_goal):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/update-kb", headers=self.__headers, json={
                    "id": id,
                    "options": options,
                    "searchGoal": search_goal
                })
                return response.text
            except Exception as err:
                print(err)

    async def remove_kb(self, id: str):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post("https://ima.kai-studio.ai/remove-kb", headers=self.__headers, json={
                    "id": id
                })
                return response.text
            except Exception as err:
                print(err)
