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
    
'''
res2= course_collection.find()

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



##This works well with mis-spelled words
query= "Operat"

res3= es_client.search(
    index="course",
    query={
        "multi_match":{
            "query": query,
            "fields": ["name", "code"],
            "fuzziness": "AUTO"
        }
    }
)

print(res3)





'''
for doc in res:
    print(doc, end= "\n")

'''

