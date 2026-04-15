from .modules.KMAudit import KMAudit
from .modules.KaiStudioCredentials import KaiStudioCredentials
from .modules.SemanticGraph import SemanticGraph
from .modules.Core import Core


class KaiStudioBackApi:
    __credentials: KaiStudioCredentials
    __km_audit: KMAudit
    __semantic_graph: SemanticGraph
    __core: Core

    def __init__(self, credentials: KaiStudioCredentials):
        self.__credentials = credentials

        if self.__credentials.organizationId and self.__credentials.instanceId and self.__credentials.apiKey:
            headers = {
                'api-key': self.__credentials.apiKey,
                'organization-id': self.__credentials.organizationId,
                'instance-id': self.__credentials.instanceId
            }

            base_url = "https://api.kai-studio.ai/"

            if self.__credentials.host:
                base_url = self.__credentials.host
                if self.__credentials.apiKey:
                    headers = {
                        'api-key': self.__credentials.apiKey
                    }
            self.__core = Core(headers, base_url)
            self.__km_audit = KMAudit(headers, base_url)
            self.__semantic_graph = SemanticGraph(headers, base_url)

    def get_credentials(self) -> KaiStudioCredentials:
        return self.__credentials

    def km_audit(self) -> KMAudit:
        return self.__km_audit

    def semantic_graph(self) -> SemanticGraph:
        return self.__semantic_graph

    def core(self) -> Core:
        return self.__core
