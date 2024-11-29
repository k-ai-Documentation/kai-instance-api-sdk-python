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

For example:
```py
core = KaiStudio(credentials).core()
print("COUNT DOCUMENTS")
print(await core.count_documents())
```

- count_documents : get number of documents analyzed

    **return** example:
    ```json
    30
    ```
- count_indexable_documents : get number of indexable document

    **return** example:
    ```json
    20
    ```
- count_indexed_documents : get number of indexed documents

    **return** example:
    ```json
    20
    ```
- count_detected_documents : get number of detected documents

    **return** example:
    ```json
    40
    ```
- download_file : download file from your knowledge base.
    >id (string): document id

- list_docs: list indexed documents

    **return** example:
    ```json
    [
        {
            "id": "Sharepoint::01Y3GAAYxxxxxxxxxx",
            "name": "Note pour XXXXXXXXX.docx"
        },
        {
            "id": "Sharepoint::01Y3GAAYxxxxxxxxxx",
            "name": "DOC 8 APRES XXXXXXXX.docx"
        },
        {
            "id": "Sharepoint::01Y3GAAYxxxxxxxxxx",
            "name": "DOC 1 Emballage XXXXXXX.docx"
        }
    ]
    ```
- differential_indexation : Index only new/updated/removed documents. It ensures that the documents are updated and their indexing reflects the latest modifications. (in progress, not finish)

### Auditing
[KMAudit.py](modules/KMAudit.py) provides methods for auditing.

For example:
```py
km_audit = KaiStudio(credentials).km_audit()
print(await km_audit.get_conflict_information(20, 0))
```

- get_conflict_information : Obtain conflict information in your knowledge base when two documents contain similar information with differences that may cause interpretation issues.
    >limit (int): 'number of content to return'

    >offset (int): 'number of content to skip before starting to collect the result set'

    **return** example:
    ```json
    [
        {
            "id": 2,
            "subject": "Valeur maximale xxxxxxxxx",
            "state": "DETECTED",
            "creation_date": "2024-09-16T13:48:15.651Z",
            "documents": [
                {
                    "docId": "Sharepoint::01Y3xxxxxxxxxxx",
                    "information_involved": "la valeur xxxxxxxxxxx"
                },
                {
                    "docId": "Sharepoint::01Y3GAxxxxxxxxxx",
                    "information_involved": "Il n'est pas nécessaire de nous xxxxxxxxxxxx"
                }
            ],
            "docsRef": [
                {
                    "id": "Sharepoint::01Y3xxxxxxxxxxx",
                    "name": "Complément produit rares.docx",
                    "url": "https://xxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx"
                },
                {
                    "id": "Sharepoint::01Y3GAxxxxxxxxxx",
                    "name": "DOC 4 Assurances.docx",
                    "url": "https://xxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx"
                }
            ]
        }
    ]
    ```
- get_duplicated_information : get back duplicated information
    >limit (int): 'number of content to return',

    >offset (int): 'number of content to skip before starting to collect the result set'

    **return** example:
    ```json
    [
        {
            "id": 2,
            "subject": "Payment options",
            "state": "DETECTED",
            "creation_date": "2024-09-16T13:48:07.222Z",
            "documents": [
                {
                    "docId": "Sharepoint::01Y3GAAY44O44Hxxxxxxxxxxx",
                    "information_involved": "Plusieurs options de xxxxxxxxxxxx"
                },
                {
                    "docId": "Sharepoint::01Y3GAAY7QA3Hxxxxxxxxxxxxxx",
                    "information_involved": "Si le destinataire xxxxxxxxxxxxxxxxx"
                }
            ],
            "docsRef": [
                {
                    "id": "Sharepoint::01Y3GAAY44O44Hxxxxxxxxxxx",
                    "name": "DIVERS.docx",
                    "url": "xxxxxxxxxxxxxxxxxxxxxxxxx"
                },
                {
                    "id": "Sharepoint::01Y3GAAY44O44Hxxxxxxxxxxx",
                    "name": "DOC 5 PAIEMENT.docx",
                    "url": "xxxxxxxxxxxxxxxxxxxxxxxxx"
                }
            ]
        },
        {
            "id": 7,
            "subject": "Couverture de base pour les pertes ou dommages jusqu'à 85€",
            "state": "DETECTED",
            "creation_date": "2024-09-16T13:48:23.736Z",
            "documents": [
                {
                    "docId": "Sharepoint::01Y3GAAYZQ3xxxxxxxxxx",
                    "information_involved": "Votre envoi bénéficie xxxxxxxxxxxx"
                },
                {
                    "docId": "Sharepoint::01Y3GAAYxxxxxxxxxxxx",
                    "information_involved": "En tout état de cause, xxxxxxxxxxxxxx"
                }
            ],
            "docsRef": [
                {
                    "id": "Sharepoint::01Y3GAAYZQ3xxxxxxxxxx",
                    "name": "DIVERS.docx",
                    "url": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                },
                {
                    "id": "Sharepoint::01Y3GAAYxxxxxxxxxxxx",
                    "name": "DOC 4 Assurances.docx",
                    "url": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                }
            ]
        }
    ]
    ```

- set_conflict_managed : set the state to managed for a conflict information
    >id (int): 'id of the conflict information to set managed'

    **return** example:
    ```json
    {
        "id": 2,
        "subject": "Valeur maximale des montres dans un colis",
        "documents": [
            {
                "docId": "Sharepoint::01Y3GAAYZQ3Oxxxxxxxxxxx",
                "information_involved": "la valeur xxxxxxxxxxxxxx"
            },
            {
                "docId": "Sharepoint::01Y3GAAYZxxxxxxxxxxxxxxx",
                "information_involved": "Il n'est pas xxxxxxxxxxxxxxxxx"
            }
        ],
        "state": "MANAGED",
        "creation_date": "2024-09-16T13:48:15.651Z"
    }
    ```

- set_duplicated_information_managed : set the state to managed for a duplicated information
    >id (int): 'id of the duplicated information to set managed'

    **return** example:
    ```json
    {
        "id": 2,
        "subject": "Payment options",
        "documents": [
            {
                "docId": "Sharepoint::01Y3GAAY44xxxxxxxxxR",
                "information_involved": "Plusieurs options xxxxxxxxxxxxxx"
            },
            {
                "docId": "Sharepoint::01Y3GAAY7QA3HMMIUExxxxxxxxxxx",
                "information_involved": "Si le destinataire xxxxxxxxxxxxxxxxxxx"
            }
        ],
        "state": "MANAGED",
        "creation_date": "2024-09-16T13:48:07.222Z"
    }
    ```

- get_documents_to_manage : List of all documents who contain conflict or duplicated information. Conflict or duplicated information have 2 state: 'DETECTED' or 'MANAGED'

    >limit (int): "number of content to skip before starting to collect the result set (default 20)"

    >offset (int): "number of content to return (default 0)"

    **return** example:
    ```json
    [
        {
            "id": "Azure Blob Storage::xxxx::e-Alerte Generalisation Facturation Electronique.pdf",
            "name": "e-Alerte Generalisation Facturation Electronique.pdf",
            "url": "/api/orchestrator/files/download?id=Azure%20Blob%20Storage%3A%3Axxxx%3A%3Ae-Alerte%20Generalisation%20Facturation%20Electronique.pdf"
        },
        {
            "id": "Azure Blob Storage::xxxx::Facturation lectronique entre entreprises pour les TPE-PME - francenum.gouv.pdf",
            "name": "Facturation lectronique entre entreprises pour les TPE-PME - francenum.gouv.pdf",
            "url": "/api/orchestrator/files/download?id=Azure%20Blob%20Storage%3A%3Axxxx%3A%3AFacturation%20lectronique%20entre%20entreprises%20pour%20les%20TPE-PME%20-%20francenum.gouv.pdf"
        },
        {
            "id": "Azure Blob Storage::xxxx::faq_fe_v30122021.pdf",
            "name": "faq_fe_v30122021.pdf",
            "url": "/api/orchestrator/files/download?id=Azure%20Blob%20Storage%3A%3Axxxx%3A%3Afaq_fe_v30122021.pdf"
        },
        {
            "id": "Azure Blob Storage::d4930e91-44fd-435a-bb33-d621af415f35::github-git-cheat-sheet_copy.pdf",
            "name": "github-git-cheat-sheet_copy.pdf",
            "url": "/api/orchestrator/files/download?id=Azure%20Blob%20Storage%3A%3Ad4930e91-44fd-435a-bb33-d621af415f35%3A%3Agithub-git-cheat-sheet_copy.pdf"
        },
        {
            "id": "Azure Blob Storage::d4930e91-44fd-435a-bb33-d621af415f35::github-git-cheat-sheet.pdf",
            "name": "github-git-cheat-sheet.pdf",
            "url": "/api/orchestrator/files/download?id=Azure%20Blob%20Storage%3A%3Ad4930e91-44fd-435a-bb33-d621af415f35%3A%3Agithub-git-cheat-sheet.pdf"
        }
    ]
    ```
- get_missing_subjects : List all missing subjects following user queries
    >limit (int): "number of content to skip before starting to collect the result set (default 20)"

    >offset (int): "number of content to return (default 0)"

    **retrun** example:
    ```json
    [
        {
            "id": 1,
            "subject": "Shipping Costs",
            "questions": [
                "combien me coûte l'envoie d'un colis de 45 m3 en angleterre ?"
            ],
            "information_needed": "- Inquiry about the cost of sending a large volume package (45 m3) to England."
        },
        {
            "id": 2,
            "subject": "Logistics",
            "questions": [
                "combien me coûte l'envoie d'un colis de 45 000 m3 en angleterre ?"
            ],
            "information_needed": "Concern related to the logistics of transporting a large volume of goods."
        },
        {
            "id": 34,
            "subject": "Envoi de colis",
            "questions": [
                "quel est le prix pour envoyer un colis de 45000 cm3 en angleterre ?"
            ],
            "information_needed": "- Inquiry about the cost of shipping a 45000 cm3 package to England.\n- Procedure for sending a 45000 cm3 package to England."
        }
    ]
    ```

### ManageInstance
[ManageInstance.py](modules/ManageInstance.py) provides methods for managing instance.

For example:
```py
manage_instance = KaiStudio(credentials).manage_instance()
print("GET GLOBAL HEALTH:")
print(await manage_instance.get_global_health())
```

- get_global_health : get global health

    **return** example:
    ```json
    "OK"
    ```
- is_api_alive : check if api is alive

    **return** example:
    ```json
    "OK"
    ```

- generate_new_api_key : generate new api key

    **return** example:
    ```json
    true
    ```

- update_name : change your instance name
    >name (string) : 'new name of your instance'

    **return** example:
    ```json
    true
    ```

- deploy : deploy your instance

    **return** example:
    ```json
    true
    ```

- delete : delete your instance 

    **return** example:
    ```json
    true
    ```

- add_kb : add knowledge base to your instance

    **return** example:
    ```json
    true
    ```

- set_playground : set playground in your instance

    **return** example:
    ```json
    true
    ```

- update-kb : update knowledge base in your instance

    **return** example:
    ```json
    true
    ```

- remove_kb : delete knowledge base in your instance
    >id (string) : 'id of knowledge base'

    **return** example:
    ```json
    true
    ```

- get_version : get version of service kai-api

    **return** example:
    ```json
    20240529
    ```

### SemanticGraph
[SemanticGraph.py](modules/SemanticGraph.py) provides methods for managing semantic graph.

For example:
```py
semantic_graph = KaiStudio(credentials).semantic_graph()
print(semantic_graph.getNodes(10,0))
```

- get_nodes : This endpoint retrieves information about semantic relationships between different concepts (nodes) in a graph. The response is an array of objects, where each object represents a relationship between two nodes. Each object contains the following fields:

        id: The unique identifier for the relationship.
        node_1: The first concept or entity in the relationship.
        node_2: The second concept or entity in the relationship.
        edge: A textual description that explains the relationship between node_1 and node_2.

    >limit (int): 'limit of elements returned'
    >offset (int): 'begin listing with this offset'

    **return** example:
    ```json
    [
        {
            "id": 1,
            "node_1": "Plantes",
            "node_2": "Boite",
            "edge": "Les plantes doivent être expédiées dans une boite\nUn dessin de fleur doit être réalisé sur le dessus du colis"
        },
        {
            "id": 2,
            "node_1": "Dessin de fleur",
            "node_2": "Livreur",
            "edge": "Le dessin de fleur permet au livreur de connaître le sens du colis lors de la livraison"
        },
        {
            "id": 3,
            "node_1": "Colis",
            "node_2": "Supplément",
            "edge": "\nThe key terms \"Colis\" and \"Supplément\" are closely related in the provided text. The text discusses various aspects of packaging and shipping colis (packages/parcels), including:\n\n- Packaging requirements for different types of items (e.g. plants, seeds, luxury watches)\n- Size and weight limitations for colis\n- Labeling and addressing requirements for colis\n- Availability of shipping labels and how to obtain them\n- Pickup and delivery options for colis\n- Insurance coverage and options for declaring higher value for colis\n\nThe text also mentions that a \"supplément\" (additional fee) of 10 euros will be charged for each colis containing flowers.\n"
        }
    ]
    ```
- get_linked_nodes : List all Nodes where the mentioned Node is present. The input « label » must be the exact name of the node_1 or node_2.
    >id (int): 'Id of the reference node'

    **return** example:
    ```json
    [
        {
            "id": 39,
            "node_1": "Colis",
            "node_2": "Restrictions de poids",
            "edge": "Packages must not weigh more than 70 kg\nPackage length must not exceed 274 cm; .........",
            "count": 4,
            "documents": [
                "Sharepoint::01Y3GAAY7QA3xxxxxxxxxxxxxxxxxxx",
                "Sharepoint::01Y3GAAY2RQWxxxxxxxxxxxxxxxxxxx",
                "Sharepoint::01Y3GAAY6MYUxxxxxxxxxxxxxxxxxxx",
                "Sharepoint::01Y3GAAYZAWOxxxxxxxxxxxxxxxxxxx"
            ]
        },
        {
            "id": 55,
            "node_1": "Colis",
            "node_2": "Perdu",
            "edge": "Un colis est considéré comme perdu s'il n'a pas été livré 24 heures après .......",
            "count": 1,
            "documents": [
                "Sharepoint::01Y3GAAY2RQWLxxxxxxxxxxxxxxxxxxx"
            ]
        }]
        ```
- get_node_by_label : Get all nodes who is involved by the label tag
    >label (string): 'Label tag'

    **return** example: 
    ```json
    [
        {
            "id": 26,
            "node_1": "UPS",
            "node_2": "United Parcel Service Belgium SA",
            "edge": "UPS is represented by United Parcel Service Belgium SA in Belgium\nUPS is represented by United Parcel Service SARL in Luxembourg\nUPS a ........",
            "count": 3,
            "documents": [
                "Sharepoint::01Y3GAAY7QA3HMMxxxxxxxxxxxxxxxxxxx",
                "Sharepoint::01Y3GAAY2WJJSYHxxxxxxxxxxxxxxxxxxx",
                "Sharepoint::01Y3GAAYZAWOE2Lxxxxxxxxxxxxxxxxxxx"
            ]
        },
        {
            "id": 46,
            "node_1": "UPS",
            "node_2": "Articles interdits",
            "edge": "UPS interdit l'envoi de certains ........",
            "count": 3,
            "documents": [
                "Sharepoint::01Y3GAAY5OMOxxxxxxxxxxxxxxxxxxx",
                "Sharepoint::01Y3GAAY7QA3xxxxxxxxxxxxxxxxxxx",
                "Sharepoint::01Y3GAAYZU6Jxxxxxxxxxxxxxxxxxxx"
            ]
        }
    ]
    ```
- detect_approximate_nodes : Identify nodes who can be used to defined the semantic context of the query. It will return all nodes that are semantically similar to the search query.
    >query (string): 'query searched'

    **return** example: 
    ```json
    [
        {
            "id": 31,
            "node_1": "UPS",
            "node_2": "Sous-traitants",
            "edge": "\nThe key information found in the extracted texts is:\n\n1. UPS is a logistics and delivery company that provides transportation services for packages, documents, and palletized goods. UPS operates through various subsidiaries in different countries, such as United Parcel Service Belgium SA, United Parcel Service France SAS, and United Parcel Service SARL in Luxembourg.\n\n2. UPS utilizes subcontractors to provide its services and can contract in its own name as well as on behalf of its employees, agents, and subcontractors, all of whom benefit from the terms and conditions.\n\n3. The transportation services provided by UPS may be subject to international conventions such as the Warsaw Convention or the CMR Convention, which can govern and limit the liability of transportation companies for loss, damage, or delay of goods.\n\n4. UPS has the right to charge late payment fees, interest, and administrative costs if the shipper, recipient, or any other party responsible for the transportation costs fails to pay the amounts due. UPS can also retain or sell the shipment to recover the unpaid debt.\n\n5. UPS is not liable for its inability to commence or continue the transport of a shipment due to events beyond its control, such as transportation disruptions, government actions, or other force majeure events.\n",
            "count": 2,
            "documents": [
                "Sharepoint::01Y3GAAY7QA3HMMIUEIVGLWNL276LLQWMX",
                "Sharepoint::01Y3GAAYZAWOE2LVGZCFFKFGGHUKYFVLC5"
            ]
        },
        {
            "id": 26,
            "node_1": "UPS",
            "node_2": "United Parcel Service Belgium SA",
            "edge": "UPS is represented by United Parcel Service Belgium SA in Belgium\nUPS is represented by United Parcel Service SARL in Luxembourg\nUPS a établi des limites de poids et de taille spécifiques pour les colis\nUPS is represented by United Parcel Service Belgium SA in Belgium\nUPS is represented by United Parcel Service SARL in Luxembourg",
            "count": 3,
            "documents": [
                "Sharepoint::01Y3GAAY7QA3HMMIUEIVGLWNL276LLQWMX",
                "Sharepoint::01Y3GAAY2WJJSYHJAYTFBLXEQTPSCDGJUO",
                "Sharepoint::01Y3GAAYZAWOE2LVGZCFFKFGGHUKYFVLC5"
            ]
        }]
        ```


### Search
[Search.py](modules/Search.py) provides methods for searching.


```py
search = KaiStudio(credentials).search()
print("RELATED FILES")
print(await search.get_list_search(0, 10))
```

- query : Make a search on the semantic index
    >query (string):  'query to search on the semantic index'

    >user (string): '(optional) user identifier to log for this query'

    >impersonate (string): 'name a profile to imitate the style of answer. eg: Knowledge manager'

    >multiDocuments (bool): 'true if you want to search across multiple documents, false if you want to retrieve an answer following only one document'
    
    >needFollowingQuestions (bool): 'true if you want to the API purpose multiple next questions, else false'

    **return** example:
    ```json
    {
        "query": "what is UPS delivery time in France ?",
        "answer": "Le délai de livraison UPS en France est de 24 heures pour les envois nationaux, que ce soit avec le service standard UPS ou UPS Access Point.",
        "reason": "Le document fournit des informations explicites sur les délais de livraison UPS en France. Il indique de manière cohérente que pour le service UPS standard et le service UPS Access Point, le délai de livraison pour les envois en France est de 24 heures.",
        "confidentRate": 0.95,
        "gotAnswer": true,
        "documents": [
            {
                "id": "Sharepoint::01Y3GAAYZFEMxxxxxxxxxxxx",
                "name": "COMPARAISON.docx",
                "url": "xxxxxxxxxxxxxxxxxxxxxxxxxx"
            }
        ],
        "followingQuestions": []
    }
    ```

- identify_specific_document : Identify a concise question following the user needs and documents from knowledge base. If in the return 'isFinal' is true, the correct question is found and you can get correct question in 'question' field. If 'isFinal' is false, you can get AI proposed question in 'question' field.
    >conversation:`an array on a conversation of the user and the assistant, each row of the array follow the structure { from: 'user' | 'assistant', message: string }`

    **return** example:
    ```json
    {
        "isFinal": true,
        "question": "What information does the UPS 2024 Service Guide for France provide?"
    }
    //in case of false
    {
        "isFinal": false,
        "question": "Pouvez-vous préciser ce que vous cherchez à savoir sur la commande SSH ?"
    }
    ```

- get_doc_signature : get back a document signature
    >id (int) : 'id of the document to get signature'

    **return** example:
    ```json
    {
        "name": "DOC 4 Assurances.docx",
        "url": "https://skillsolutionsoftware.sharepoint.com/sites/Skillbase-KAI/_layouts/15/Doc.aspx?sourcedoc=%7B6CA0DB30-C3F8-404D-82DF-C396F747176A%7D&file=DOC%204%20Assurances.docx&action=default&mobileredirect=true",
        "document": {
            "id": "Sharepoint::01Y3GAAYZQ3OQGZ6GDJVAIFX6DS33UOF3K",
            "name": "DOC 4 Assurances.docx",
            "extraproperties": {
                "id": "01Y3GAAYZQ3OQGZ6GDJVAIFX6DS33UOF3K",
                "cTag": "\"c:{6CA0DB30-C3F8-404D-82DF-C396F747176A},2\"",
                "eTag": "\"{6CA0DB30-C3F8-404D-82DF-C396F747176A},1\"",
                "file": {
                    "hashes": {
                        "quickXorHash": "S3IkNDfzFTntRKk90ttbIB2/PJw="
                    },
                    "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                },
                "name": "DOC 4 Assurances.docx",
                "size": 21772,
                "shared": {
                    "scope": "users"
                },
                "webUrl": "https://skillsolutionsoftware.sharepoint.com/sites/Skillbase-KAI/_layouts/15/Doc.aspx?sourcedoc=%7B6CA0DB30-C3F8-404D-82DF-C396F747176A%7D&file=DOC%204%20Assurances.docx&action=default&mobileredirect=true",
                "createdBy": {
                    "user": {
                        "id": "7b51bc72-3609-4f5a-90dc-dc092bef6ef9",
                        "email": "sngo@wats.ai",
                        "displayName": "Stephane NGO"
                    }
                },
                "kb_signature": {
                    "name": "Skillbase-KAI::KAI/KAI DEMO V2 - Instances/LVMH DEMO",
                    "type": "SharepointKnowledgeBase"
                },
                "fileSystemInfo": {
                    "createdDateTime": "2024-06-07T15:08:17Z",
                    "lastModifiedDateTime": "2024-06-07T15:08:17Z"
                },
                "lastModifiedBy": {
                    "user": {
                        "id": "7b51bc72-3609-4f5a-90dc-dc092bef6ef9",
                        "email": "sngo@wats.ai",
                        "displayName": "Stephane NGO"
                    }
                },
                "createdDateTime": "2024-06-07T15:08:17Z",
                "parentReference": {
                    "id": "01Y3GAAYZ6BZX3D5FZRJEJXM454S3M6UEN",
                    "name": "LVMH DEMO",
                    "path": "/drives/b!GizPr4fHx0-m8l-A_iIpSRdsr1PHDJBBvgIFWrKoORA1hRhJ_-lnR7uaI0AYJTJp/root:/KAI/KAI DEMO V2 - Instances/LVMH DEMO",
                    "siteId": "afcf2c1a-c787-4fc7-a6f2-5f80fe222949",
                    "driveId": "b!GizPr4fHx0-m8l-A_iIpSRdsr1PHDJBBvgIFWrKoORA1hRhJ_-lnR7uaI0AYJTJp",
                    "driveType": "documentLibrary"
                },
                "lastModifiedDateTime": "2024-06-07T15:08:17Z",
                "@microsoft.graph.downloadUrl": "https://skillsolutionsoftware.sharepoint.com/sites/Skillbase-KAI/_layouts/15/download.aspx?UniqueId=6ca0db30-c3f8-404d-82df-c396f747176a&Translate=false&tempauth=v1.eyJzaXRlaWQiOiJhZmNmMmMxYS1jNzg3LTRmYzctYTZmMi01ZjgwZmUyMjI5NDkiLCJhcHBfZGlzcGxheW5hbWUiOiJhdWRpdC1rbSIsImF1ZCI6IjAwMDAwMDAzLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMC9za2lsbHNvbHV0aW9uc29mdHdhcmUuc2hhcmVwb2ludC5jb21AZmZiNzRlMzYtNTRjZC00YmJmLThhNDQtMDg3ZjU4YjJjMGQzIiwiZXhwIjoiMTcyNjQ5Nzc5OCJ9.CgoKBHNuaWQSAjY0EgsIuKK55fGXqz0QBRoNMjAuMTkwLjE3Ny4yNSosdjlRZTRZSW45TDNvcVpUM0Zlb0srbjN0dXc0ZnJaQTdpUXU3MWkyYUpEcz0wmAE4AUIQoVDT-kJQAJDhsAHFsZ2f4koQaGFzaGVkcHJvb2Z0b2tlbnoBMboBJmdyb3VwLnJlYWQgYWxsc2l0ZXMucmVhZCBhbGxmaWxlcy5yZWFkwgFJODQ4ZTVjNTEtZGExYS00NmU1LWJiM2ItNTQxN2JjYWYxYzc1QGZmYjc0ZTM2LTU0Y2QtNGJiZi04YTQ0LTA4N2Y1OGIyYzBkM8gBAQ.m2aA0M-ZcqhvH5GCROaZlDh6ypteCPmHxcHlaoWYo3k&ApiVersion=2.0"
            }
        }
    }
    ```

- get_doc_ids : get back identified documents signature (name and url)
    >docsIds (list): 'all docs ids'

    **return** example:
    ```json
    [
        {
            "id": "Sharepoint::01Y3GAAYZ2L5MNAxxxxxxx",
            "name": "Complément produit rares.docx",
            "url": "https://xxxxxxxxxxx.xxxxxxxxx.xxxxxxxxxxx"
        },
        {
            "id": "Sharepoint::01Y3GAAYYWAQDJ6xxxxxxx",
            "name": "contact en image.pdf",
            "url": "https://xxxxxxxxxxx.xxxxxxxxx.xxxxxxxxxxx"
        }
    ]
    ```
- count_done_requests : count number of call on search (/query) endpoint

    **return** example:
    ```json
    90
    ```
- count_answered_done_requests : count number of call on search (/query) endpoint where KAI find an answer

    **return** example:
    ```json
    80
    ```
- get_requests_to_api : History of searches performed since the beginning in ascending order. A pagination system can be created with the offset value, limit per query value.
    >limit (int): 'number of content to return'
                    
    >offset (int): 'number of content to skip before starting to collect the result set'

    **return** example:
    ```json
    [
        {
            "id": 1,
            "query": "Note pour l’ivoire",
            "answer_text": "La note pour l'ivoire est un message d'avertissement sur un colis. Le message, écrit en français, indique que le colis peut contenir de l'ivoire et doit être manipulé avec précaution. Cette information est représentée visuellement par une icône de colis.",
            "user_id": ""
        },
        {
            "id": 2,
            "query": "quelles sont les heures d'ouverture du service client ?",
            "answer_text": "Selon nos documents, il y a deux informations différentes concernant les heures d'ouverture du service client :\n\n1. Une source indique que le service client est disponible de 8h à 21h du lundi au vendredi, et fermé le samedi.\n\n2. Une autre source mentionne des horaires différents : du lundi au vendredi de 8h00 à 19h00, et le samedi de 8h00 à 13h00.\n\nEn raison de cette discordance, il serait préférable de contacter directement le service client pour obtenir les horaires les plus à jour.",
            "user_id": ""
        },
        {
            "id": 3,
            "query": "quelles sont les heures d'ouverture du service client ?",
            "answer_text": "Selon nos documents, il y a deux informations différentes concernant les heures d'ouverture du service client :\n\n1. Une source indique que le service client est disponible de 8h à 21h du lundi au vendredi, et fermé le samedi.\n\n2. Une autre source mentionne des horaires différents : du lundi au vendredi de 8h00 à 19h00, et le samedi de 8h00 à 13h00.\n\nEn raison de cette discordance, il serait préférable de contacter directement le service client pour obtenir les horaires les plus à jour.",
            "user_id": ""
        }]
    ```



<u>**For more examples, you can check the [example.py](example.py) file.**</u>

## Contributing
bxu@k-ai.ai

rmei@k-ai.ai

sngo@k-ai.ai

