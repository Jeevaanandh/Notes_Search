from pymongo import MongoClient
from elasticsearch import Elasticsearch

MONGO_URI= "mongodb://localhost:27017/"

mongo_client = MongoClient(MONGO_URI)
es_client= Elasticsearch("http://localhost:9200")


db= mongo_client["Notes_Search"]

course_collection= db["course"]
notes_collection= db["notes"]

res1= notes_collection.find()

'''
for doc in res:
    print(doc, end="\n")
'''

res2= course_collection.find()
    
'''
# Adding the document with the details we need to Elastic Search
for doc in res2:
    es_client.index(
        index= "course",
        id= str(doc["_id"]),
        document={
            "name": doc["name"],
            "code": doc["code"]
        }
    )

'''

# Creating a new index for n-gram-search


'''
es_client.indices.create(
    index="course2",
    body={
        "settings": {
            "index.max_ngram_diff": 7,   
            "analysis": {
                "tokenizer": {
                    "ngram_tokenizer": {
                        "type": "ngram",
                        "min_gram": 3,
                        "max_gram": 10,
                        "token_chars": ["letter", "digit"]
                    }
                },
                "analyzer": {
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "ngram_tokenizer",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "name": {
                    "type": "text",
                    "analyzer": "ngram_analyzer",
                    "search_analyzer": "standard"
                },
                "code": {
                    "type": "text",
                    "analyzer": "ngram_analyzer",
                    "search_analyzer": "standard"
                }
            }
        }
    }
)
'''

for doc in res2:
    es_client.index(
        index= "course2",
        id= str(doc["_id"]),
        document={
            "name": doc["name"],
            "code": doc["code"]
        }
    )


##This works well with mis-spelled words
query= "BCS"

res3= es_client.search(
    index="course2",
    query={
        "multi_match":{
            "query": query,
            "fields": ["name", "code"],
            
        }
    }
)

print(res3["hits"]["hits"])





'''
for doc in res:
    print(doc, end= "\n")

'''

