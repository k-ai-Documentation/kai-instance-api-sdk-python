import httpx


class Chatbot:
    """
    A chatbot client for interacting with the API.
    """

    def __init__(self, headers: dict, base_url: str):
        """
        Initialize the Chatbot instance.

        :param headers: HTTP headers for API requests.
        :param base_url: Base URL of the chatbot API.
        """
        self.__baseurl = base_url
        self.__headers = headers

    async def get_full_conversation(self, conversation_id: str) -> dict:
        """
        Retrieve the full conversation history.

        :param conversation_id: The ID of the conversation to retrieve.
        :return: The conversation history as a dictionary.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/chatbot/get-conversation",
                    headers=self.__headers,
                    json={"id": conversation_id}
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)

    async def conversation(self, conversation_id: str, user_message: str, multi_documents: bool, user_id: str) -> dict:
        """
        Send a user message and get a chatbot response.

        :param conversation_id: The ID of the conversation.
        :param user_message: The user's message to the chatbot.
        :param multi_documents: Whether to search across multiple documents.
        :param user_id: The user identifier.
        :return: The chatbot's response as a dictionary.
        """
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            try:
                response = await client.post(
                    f"{self.__baseurl}api/chatbot/message",
                    headers=self.__headers,
                    json={
                        "id": conversation_id,
                        "user_message": user_message,
                        "multi_documents": multi_documents,
                        "user_id": user_id
                    }
                )
                return response.json()['response'] if response.status_code == 200 else response.text
            except Exception as err:
                print(err)
