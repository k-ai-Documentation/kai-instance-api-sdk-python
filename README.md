# sdk-python

## Introduction
SDK python enables developers to efficiently manage files, instance, perform searches, handle thematic content, and conduct audits. This toolkit is designed to streamline the integration of complex functionalities into python-based projects.

## Installation
You have 3 ways to install sdk_python in your project:
1. You can install it via pip:
```
pip install git+https://github.com/k-ai-Documentation/sdk-python.git@version2.0
```
then you can import the SDK in your project:
```python
from kai_sdk_python.index import KaiStudio, KaiStudioCredentials
```
2. You can install it via requirements.txt:
add this line in your requirements.txt file:
```
git+https://github.com/k-ai-Documentation/sdk-python.git@version2.0
```
then you can install it via pip:
```
pip install -r requirements.txt
```
then you can import the SDK in your project:
```python
from kai_sdk_python.index import KaiStudio, KaiStudioCredentials
```
3. You can clone the repository and install it manually:

To integrate the SDK into your project, include the SDK files in your project directory. 

then you can import the SDK in your project:
```python
from your_repo.kai_sdk_python.index import KaiStudio, KaiStudioCredentials
```

## Quick start
There are two type of versions: SaaS version and Premise version.

#### SaaS version

SaaS version means you are using the service provided by Kai with cloud service. In this case, you will need 3 keys (organizationId, instanceId, apiKey) to initialize kaiStudio.

Here's a simple example to get you started with the SDK:

```
from kai_sdk_python.index import KaiStudio
from kai_sdk_python.index import KaiStudioCredentials

credentials = KaiStudioCredentials({organizationId="your organization id",
                                   instanceId="your instance id",
                                   apiKey="your api key"})
search = KaiStudio(credentials).search()
print("SEARCH QUERY:")
print(await search.query("what is the history of France TV?", "userid"))

```
#### Premise version

Premise version means you are using the service in your local server in your enterprise. In this case, you will need host and api key (optional) to initialize kaiStudio.

Here's a simple example to get you started with the SDK:

```
from kai_sdk_python.index import KaiStudio
from kai_sdk_python.index import KaiStudioCredentials

//apiKey is optionnal
credentials = KaiStudioCredentials({host="your server host", apiKey="your api key"})
search = KaiStudio(credentials).search()
print("SEARCH QUERY:")
print(await search.query("what is the history of France TV?", "userid"))

```

## Usage Guide
### Core
[Core.py](modules/Core.py) provides methods for core functionalities.
- count_documents : get number of documents analyzed
- count_indexable_documents : get number of indexable document
- count_indexed_documents : get number of indexed documents
- count_detected_documents : get number of detected documents
- download_file : download file
    >id: document id
- differential_indexation : index only new/updated/removed documents

For example:
```py
core = KaiStudio(credentials).core()
print("COUNT DOCUMENTS")
print(await core.count_documents())
```

### Auditing
[KMAudit.py](modules/KMAudit.py) provides methods for auditing.

- get_conflict_information : get back conflict information
    >limit: 'number of content to return'

    >offset: 'number of content to skip before starting to collect the result set'
- get_duplicated_information : get back duplicated information
    >limit: 'number of content to return',

    >offset: 'number of content to skip before starting to collect the result set'

- set_conflict_managed : set the state to managed for a conflict information
    >id: 'id of the conflict information to set managed'

- set_duplicated_information_managed : set the state to managed for a duplicated information
    >id: 'id of the duplicated information to set managed'

- get_documents_to_manage : list of all documents who contain conflict or duplicated information
    >limit: "number of content to skip before starting to collect the result set (default 20)"

    >offset: "number of content to return (default 0)"
- get_missing_subjects : List all missing subjects following user queries
    >limit: "number of content to skip before starting to collect the result set (default 20)"

    >offset: "number of content to return (default 0)"

For example:
```py
km_audit = KaiStudio(credentials).km_audit()
print(await km_audit.get_conflict_information(20, 0))
```

### ManageInstance
[ManageInstance.py](modules/ManageInstance.py) provides methods for managing instance.
- get_global_health : get global health
- is_api_alive : check if api is alive
- version : get version

For example:
```py
manage_instance = KaiStudio(credentials).manage_instance()
print("GET GLOBAL HEALTH:")
print(await manage_instance.get_global_health())
```

### SemanticGraph
[SemanticGraph.py](modules/SemanticGraph.py) provides methods for managing semantic graph.
- get_nodes : list all generated semantic nodes
    >limit: 'limit of elements returned'
    >offset: 'begin listing with this offset'
- get_linked_nodes : get all linked nodes of one selected node
    >id: 'Id of the reference node'
- get_node_by_label : Get all nodes who is involved by the label tag
    >label: 'Label tag'
- detect_approximate_nodes : Identify nodes who can be used to defined the semaantic context of the query
    >query: 'query searched'


For example:
```py
semantic_graph = KaiStudio(credentials).semantic_graph()
print(semantic_graph.getNodes(10,0))
```

### Search
[Search.py](modules/Search.py) provides methods for searching.
- query : Make a search on the semantic index
    >query: 'query to search on the semantic index'

    >user: '(optional) user identifier to log for this query'

    >impersonate: 'name a profile to imitate the style of answer. eg: Knowledge manager or Sales man'

    >multiDocuments: 'true if you want to search across multiple documents, false if you want to retrieve an answer following only one document'
    
    >needFollowingQuestions: 'true if you want to the API purpose multiple next questions, else false'

- get_doc_signature : get back a document signature
    >id: 'id of the document to get signature'

- get_doc_ids : get back identified documents signature
    >docsIds: 'all docs ids'

- count_done_requests : count number of call on search (/query) endpoint
- count_answered_done_requests : count number of call on search (/query) endpoint where KAI find an answer
- get_requests_to_api : get back requests made to the API
    >limit: 'number of content to return'
                    
    >offset: 'number of content to skip before starting to collect the result set'
- identify_specific_document : identify a concise question following the user needs and documents from knowledge base
    >conversation:`an array on a conversation of the user and the assistant, each row of the array follow the structure { from: 'user' | 'assistant', message: string }`


```py
search = KaiStudio(credentials).search()
print("RELATED FILES")
print(await search.get_list_search(0, 10))
```


<u>**For more examples, you can check the [example.py](example.py) file.**</u>

## Contributing
bxu@k-ai.ai

rmei@k-ai.ai

sngo@k-ai.ai

