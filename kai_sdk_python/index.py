from dataclasses import dataclass
from enum import Enum

from .modules.http_client import RetryOptions
from .modules.document import Document
from .modules.orchestrator import Orchestrator
from .modules.semantic_graph import SemanticGraph
from .modules.km_audit import KMAudit


class State(str, Enum):
    """Document lifecycle states, from initial ingestion through full indexation."""

    PARSING_ERROR = "PARSING_ERROR"
    INITIAL_SAVED = "INITIAL_SAVED"
    UPDATED = "UPDATED"
    ON_CONTENT_EXTRACT = "ON_CONTENT_EXTRACT"
    CONTENT_EXTRACTED = "CONTENT_EXTRACTED"
    ON_INDEXATION = "ON_INDEXATION"
    INDEXED = "INDEXED"


@dataclass
class KaiStudioCredentials:
    """Authentication and routing credentials for a KAI Studio instance.

    All fields default to empty string. Only non-empty fields are sent as request headers.

    Attributes:
        api_key: Sent as the ``api-key`` header.
        instance_id: Sent as the ``instance-id`` header.
        host: Overrides the base URL (default ``https://api.kai-studio.ai/``).
        api_host: Sent as the ``api-host`` header.
    """

    api_key: str = ""
    instance_id: str = ""
    host: str = ""
    api_host: str = ""


class KaiInstanceApi:
    """Factory and entry point for the KAI Studio SDK.

    Instantiate with :class:`KaiStudioCredentials`, then access modules via
    the getter methods.

    Example::

        credentials = KaiStudioCredentials(api_key="...", instance_id="...")
        api = KaiInstanceApi(credentials)
        docs = await api.document().list_documents()
    """

    def __init__(self, credentials: KaiStudioCredentials, retry_options: RetryOptions | None = None):
        """Initialise the API client and all sub-modules.

        Args:
            credentials: Authentication and routing details for the target instance.
            retry_options: Optional retry/timeout configuration. Falls back to
                :class:`~kai_sdk_python.modules.http_client.RetryOptions` defaults.
        """
        headers = {}
        if credentials.api_key:
            headers["api-key"] = credentials.api_key
        if credentials.instance_id:
            headers["instance-id"] = credentials.instance_id
        if credentials.api_host:
            headers["api-host"] = credentials.api_host

        base_url = credentials.host or "https://api.kai-studio.ai/"

        self._document = Document(headers, base_url, retry_options)
        self._orchestrator = Orchestrator(headers, base_url, retry_options)
        self._semantic_graph = SemanticGraph(headers, base_url, retry_options)
        self._audit_instance = KMAudit(headers, base_url, retry_options)

    def document(self) -> Document:
        """Return the Document module for listing, retrieving, and downloading documents."""
        return self._document

    def orchestrator(self) -> Orchestrator:
        """Return the Orchestrator module for triggering indexation and monitoring background tasks."""
        return self._orchestrator

    def semantic_graph(self) -> SemanticGraph:
        """Return the SemanticGraph module for querying knowledge-graph nodes."""
        return self._semantic_graph

    def audit_instance(self) -> KMAudit:
        """Return the KMAudit module for conflict anomaly detection and management."""
        return self._audit_instance

