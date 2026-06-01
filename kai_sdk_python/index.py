from dataclasses import dataclass
from enum import Enum

from .modules.http_client import RetryOptions
from .modules.document import Document
from .modules.orchestrator import Orchestrator
from .modules.semantic_graph import SemanticGraph
from .modules.km_audit import KMAudit


class State(str, Enum):
    PARSING_ERROR = "PARSING_ERROR"
    INITIAL_SAVED = "INITIAL_SAVED"
    UPDATED = "UPDATED"
    ON_CONTENT_EXTRACT = "ON_CONTENT_EXTRACT"
    CONTENT_EXTRACTED = "CONTENT_EXTRACTED"
    ON_INDEXATION = "ON_INDEXATION"
    INDEXED = "INDEXED"


@dataclass
class KaiStudioCredentials:
    api_key: str = ""
    instance_id: str = ""
    host: str = ""
    authorization: str = ""
    api_host: str = ""


class KaiInstanceApi:
    def __init__(self, credentials: KaiStudioCredentials, retry_options: RetryOptions | None = None):
        self._credentials = credentials
        headers = {}
        if credentials.api_key:
            headers["api-key"] = credentials.api_key
        if credentials.instance_id:
            headers["instance-id"] = credentials.instance_id
        if credentials.authorization:
            headers["Authorization"] = credentials.authorization
        if credentials.api_host:
            headers["api-host"] = credentials.api_host

        base_url = credentials.host or "https://api.kai-studio.ai/"

        self._document = Document(headers, base_url, retry_options)
        self._orchestrator = Orchestrator(headers, base_url, retry_options)
        self._semantic_graph = SemanticGraph(headers, base_url, retry_options)
        self._audit_instance = KMAudit(headers, base_url, retry_options)

    def document(self) -> Document:
        return self._document

    def orchestrator(self) -> Orchestrator:
        return self._orchestrator

    def semantic_graph(self) -> SemanticGraph:
        return self._semantic_graph

    def audit_instance(self) -> KMAudit:
        return self._audit_instance

    def get_credentials(self) -> KaiStudioCredentials:
        return self._credentials
