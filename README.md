# sdk-python

## Introduction

SDK python enables developers to efficiently manage files, instance, perform searches, handle thematic content, and
conduct audits. This toolkit is designed to streamline the integration of complex functionalities into python-based
projects.

## Installation

To integrate the SDK into your project, include the SDK files in your project directory.

## Quick start

There are two type of versions: SaaS version and Premise version.

#### SaaS version

SaaS version means you are using the service provided by Kai with cloud service. In this case, you will need 3 keys (
organizationId, instanceId, apiKey) to initialize kaiStudio.

Here's a simple example to get you started with the SDK:

```
from index import KaiStudio
from index import KaiStudioCredentials

credentials = KaiStudioCredentials({organizationId="your organization id",
                                   instanceId="your instance id",
                                   apiKey="your api key"})
search = KaiStudio(credentials).search()
print("SEARCH QUERY:")
print(await search.query("what is the history of France TV?", "userid"))

```

#### Premise version

Premise version means you are using the service in your local server in your enterprise. In this case, you will need
host and api key (optional) to initialize kaiStudio.

Here's a simple example to get you started with the SDK:

```
from index import KaiStudio
from index import KaiStudioCredentials

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
- count_in_progress_indexation_documents: get number of in progress indexation documents
- download_file : download file
  > id: document id
- list_docs : list documents
- differential_indexation : index only new/updated/removed documents
- last_indexation_begin_time : Get last indexation begin time
- last_indexation_end_time : Get last indexation end time
- list_indexed_documents : list indexed documents
  > limit: 'number of content to return'

  > offset: 'number of content to skip before starting to collect the result set'
- get_scenarios : List all available scenarios with theirs API signatures
- get_logs : Get KAI Semantic layer logs
  log types: LLM error 500, LLM error 503, LLM Limitation rate, Application information, Excel parser error, Ppt Parser
  error, Word Parser error, Image Parser error, PDF Parser Error, Markdown Parser Error, Html Parser Error
  > type: `type of log you want (like'Application information'), dont add if you want to get back all logs`

  > skip: 'pagination skip elements'

  > take: 'pagination take elements'
- reinit_all : Hard reset of KAI Semantic layer and reindex all datas, it can take a lot of time depending on the size
  of databases connected to KAI
- check_pedding_job : Get the information about your instance background jobs in progress.

    Available values :
    
    "Indexation in progress" , "Partial indexation in progress" , "Recovery indexation in progress" : An indexation of new or updated documents is pending.

    "Loading Audit" : "Audit of the indexed documents is pending.

For example:

```py
core = KaiStudio(credentials).core()
print("COUNT DOCUMENTS")
print(await core.count_documents())
```

### Auditing

[KMAudit.py](modules/KMAudit.py) provides methods for auditing.

- get_conflict_information : get back conflict information
  > limit: 'number of content to return'

  > offset: 'number of content to skip before starting to collect the result set'

  > query: 'query string'

- get_duplicated_information : get back duplicated information
  > limit: 'number of content to return',

  > offset: 'number of content to skip before starting to collect the result set'

  > query: 'query string'

- set_conflict_managed : set the state to managed for a conflict information
  > id: 'id of the conflict information to set managed'

- set_duplicated_information_managed : set the state to managed for a duplicated information
  > id: 'id of the duplicated information to set managed'

- get_documents_to_manage : list of all documents who contain conflict or duplicated information
  > limit: "number of content to skip before starting to collect the result set (default 20)"

  > offset: "number of content to return (default 0)"
- get_missing_subjects : List all missing subjects following user queries
  > limit: "number of content to skip before starting to collect the result set (default 20)"

  > offset: "number of content to return (default 0)"
- get_anomalies_for_doc : get back anomalies (conflict and duplicated information) for a document
  > doc_id: 'id of the document'
- count_missing_subjects : count missing subjects
- count_duplicated_information : count duplicated information
- count_conflict_information : count conflict information

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
  > limit: 'limit of elements returned'
  > offset: 'begin listing with this offset'
- get_linked_nodes : get all linked nodes of one selected node
  > id: 'Id of the reference node'
- get_node_by_label : Get all nodes who is involved by the label tag
  > label: 'Label tag'
- detect_approximal_nodes : Identify nodes who can be used to defined the semaantic context of the query
  > query: 'query searched'
  > need_documents_content: 'whether response contains content' 

For example:

```py
semantic_graph = KaiStudio(credentials).semantic_graph()
print(semantic_graph.getNodes(10, 0))
```

### Search

[Search.py](modules/Search.py) provides methods for searching.

- query : Make a search on the semantic index
  > query: 'query to search on the semantic index'

  > user: '(optional) user identifier to log for this query'

  > impersonate: 'name a profile to imitate the style of answer. eg: Knowledge manager or Sales man'

  > multiDocuments: 'true if you want to search across multiple documents, false if you want to retrieve an answer
  following only one document'

  > needFollowingQuestions: 'true if you want to the API purpose multiple next questions, else false'

- get_doc_signature : get back a document signature
  > id: 'id of the document to get signature'

- get_doc_ids : get back identified documents signature
  > docsIds: 'all docs ids'

- count_done_requests : count number of call on search (/query) endpoint
- count_answered_done_requests : count number of call on search (/query) endpoint where KAI find an answer
- get_requests_to_api : get back requests made to the API
  > limit: 'number of content to return'

  > offset: 'number of content to skip before starting to collect the result set'
- identify_specific_document : identify a concise question following the user needs and documents from knowledge base
  > conversation:
  `an array on a conversation of the user and the assistant, each row of the array follow the structure { from: 'user' | 'assistant', message: string }`

```py
search = KaiStudio(credentials).search()
print("RELATED FILES")
print(await search.get_list_search(0, 10))
```

### Chatbot

[Chatbot](modules/Chatbot.py) provides methods for chatting.

- getFullConversation : list all conversations of a given id
  > id: id of conversation
- conversation :
  > id:[string] conversation id, for first message no id needed
  >
  >user_message: [string] user last message
  >
  >multi_documents: [boolean] search with multiple documents
  >
  >user_id: [string] (optional) user id to identify the user question in logs parts

For example:

```python
chatbot = KaiStudio(credentials).chatbot()
print("GET FULL CONVERSATION")
print(await chatbot.get_full_conversation("xxxxxx"))
```

<u>**For more examples, you can check the [example.py](example.py) file.**</u>

## Contributing

bxu@k-ai.ai

rmei@k-ai.ai

sngo@k-ai.ai
