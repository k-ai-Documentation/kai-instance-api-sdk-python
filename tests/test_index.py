from kai_sdk_python.index import KaiInstanceApi, KaiStudioCredentials, RetryOptions, State
from kai_sdk_python.modules.document import Document
from kai_sdk_python.modules.orchestrator import Orchestrator
from kai_sdk_python.modules.semantic_graph import SemanticGraph
from kai_sdk_python.modules.km_audit import KMAudit


def test_state_enum_values():
    assert State.PARSING_ERROR == "PARSING_ERROR"
    assert State.INITIAL_SAVED == "INITIAL_SAVED"
    assert State.UPDATED == "UPDATED"
    assert State.ON_CONTENT_EXTRACT == "ON_CONTENT_EXTRACT"
    assert State.CONTENT_EXTRACTED == "CONTENT_EXTRACTED"
    assert State.ON_INDEXATION == "ON_INDEXATION"
    assert State.INDEXED == "INDEXED"


def test_default_base_url():
    creds = KaiStudioCredentials(api_key="k", instance_id="i")
    api = KaiInstanceApi(creds)
    assert api.document()._http._base_url == "https://api.kai-studio.ai/"


def test_custom_host_overrides_base_url():
    creds = KaiStudioCredentials(host="https://my-server.example.com/")
    api = KaiInstanceApi(creds)
    assert api.document()._http._base_url == "https://my-server.example.com/"


def test_headers_include_api_key():
    creds = KaiStudioCredentials(api_key="my-key")
    api = KaiInstanceApi(creds)
    assert api.document()._http._headers.get("api-key") == "my-key"


def test_headers_include_instance_id():
    creds = KaiStudioCredentials(instance_id="my-instance")
    api = KaiInstanceApi(creds)
    assert api.document()._http._headers.get("instance-id") == "my-instance"



def test_headers_include_api_host():
    creds = KaiStudioCredentials(api_host="proxy.example.com")
    api = KaiInstanceApi(creds)
    assert api.document()._http._headers.get("api-host") == "proxy.example.com"


def test_empty_credential_fields_excluded_from_headers():
    creds = KaiStudioCredentials(api_key="k")  # all others default to ""
    api = KaiInstanceApi(creds)
    headers = api.document()._http._headers
    assert "instance-id" not in headers
    assert "api-host" not in headers


def test_module_accessors_return_correct_types():
    creds = KaiStudioCredentials(api_key="k")
    api = KaiInstanceApi(creds)
    assert isinstance(api.document(), Document)
    assert isinstance(api.orchestrator(), Orchestrator)
    assert isinstance(api.semantic_graph(), SemanticGraph)
    assert isinstance(api.audit_instance(), KMAudit)


def test_module_accessors_return_same_instance():
    creds = KaiStudioCredentials(api_key="k")
    api = KaiInstanceApi(creds)
    assert api.document() is api.document()
    assert api.orchestrator() is api.orchestrator()
    assert api.semantic_graph() is api.semantic_graph()
    assert api.audit_instance() is api.audit_instance()



def test_retry_options_forwarded_to_modules():
    creds = KaiStudioCredentials(api_key="k")
    opts = RetryOptions(max_retries=5, retry_delay=2.0, timeout=60.0)
    api = KaiInstanceApi(creds, opts)
    assert api.document()._http._max_retries == 5
    assert api.document()._http._retry_delay == 2.0
