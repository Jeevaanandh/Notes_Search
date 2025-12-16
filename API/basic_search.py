from pymongo import MongoClient
from elasticsearch import Elasticsearch


mongo= MongoClient("mongodb://localhost:27017/")
es= Elasticsearch("http://localhost:9200/")

db= mongo["Notes_Search"]
course= db["course"]
notes= db["notes"]



# This approach works well with complete words that are mis-spelled

def search(query):
    res= es.search(   # Searching in the "course" index
        index="course",
        query={
            "multi_match":{
                "query": query,
                "fields": ["name", "code"],
                "fuzziness": "AUTO"
            }
        }
    )

    hits= res["hits"]["hits"]

    
    if(len(hits)!=0):
        doc= hits[0]["_source"]   #This returns the actual MongoDb Document. 

        doc= notes.find({"code": doc["code"]})

        response= doc

        return response     #Returning the document deom the notes collection after searching.
    
    else:
        return []



ans=search("Opearaiting")

if not ans:
    print("Not found, check the spelling...")

for i in ans:

    print(i)