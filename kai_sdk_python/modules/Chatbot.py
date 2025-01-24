import httpx


class Chatbot:

    def __init__(self, headers, base_url):
        self.__baseurl = base_url
        self.__headers = headers

    async def get_full_conversation(self, conversation_id):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/chatbot/get-conversation", headers=self.__headers,
                                             json={
                                                 "id": conversation_id
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def conversation(self, conversation_id, user_message, multi_documents, user_id):
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(self.__baseurl + "api/chatbot/message",
                                             headers=self.__headers,
                                             json={
                                                 "conversation_id": conversation_id,
                                                 "user_message": user_message,
                                                 "multi_documents": multi_documents,
                                                 "user_id": user_id
                                             })
                return response.json() if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
