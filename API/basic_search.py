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

    response="Not Found, Check Spelling"

    if(len(hits)!=0):
        response= hits[0]["_source"]   #This returns the actual MongoDb Document. 

    return response



ans=search("Dratabase")
print(ans)