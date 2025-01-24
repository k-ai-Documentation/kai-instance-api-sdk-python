import asyncio

from kai_sdk_python.index import KaiStudio
from kai_sdk_python.index import KaiStudioCredentials

credentials = KaiStudioCredentials(organizationId="xxxxxxx",
                                   instanceId="xxxxxxx",
                                   apiKey="xxxxxx")

manage_instance = KaiStudio(credentials).manage_instance()
search = KaiStudio(credentials).search()
km_audit = KaiStudio(credentials).km_audit()
semantic_graph = KaiStudio(credentials).semantic_graph()
core = KaiStudio(credentials).core()
chatbot = KaiStudio(credentials).chatbot()


async def sync_mode():
    print("GET FULL CONVERSATION")
    print(await chatbot.get_full_conversation("xxxxxx"))

    print("SEND MESSAGE")
    print(await chatbot.conversation("", "xxxxxxxxxxxxx", False, "xxxxxxxxxxxxxxxxxxx"))


if __name__ == "__main__":
    asyncio.run(sync_mode())
