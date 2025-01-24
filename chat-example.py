import asyncio

from kai_sdk_python.index import KaiStudio
from kai_sdk_python.index import KaiStudioCredentials

credentials = KaiStudioCredentials(organizationId="c977644b-8b4a-43ee-8901-a609ef3b9e19",
                                   instanceId="03fb090f-b2ac-444a-8356-6be9d9fe132a",
                                   apiKey="TTLM0qFAT9FTXk/i6uvwh8IbU3jLw9/zMXvdSul2/E0=")

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
