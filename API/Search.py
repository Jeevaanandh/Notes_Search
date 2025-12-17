from pymongo import MongoClient
from elasticsearch import Elasticsearch


mongo= MongoClient("mongodb://localhost:27017/")
es= Elasticsearch("http://localhost:9200/")

db= mongo["Notes_Search"]
course= db["course"]
notes= db["notes"]



# This approach works well with complete words that are mis-spelled

def basic_search(query):
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
    



def NGramSearch(query):
    res= es.search(
        index="course2",
        query={
            "multi_match":{
                "query": query,
                "fields": ["name", "code"],
                
            }
        }
    )

    hits= res["hits"]["hits"]

    
    if(len(hits)!=0):
        response=[]
        temp=[]
        for i in hits:
            temp.append(i["_source"])#This returns the actual MongoDb Document from course collection 

        for j in temp:
            doc= notes.find({"code": j["code"]})

            for k in doc:
                response.append(k)

        return response     #Returning the document deom the notes collection after searching.
    
    else:
        return []
    


#This is used to help with auto fill. 
#Call this endpoint whenever the search box has more than three characters
# If the response returned is empty, no matching results were found.
def NGramSearch_Box(query):
    res= es.search(
        index="course2",
        size=5,
        query={
            "multi_match":{
                "query": query,
                "fields": ["name", "code"],
                
            }
        }
    )

    hits= res["hits"]["hits"]

    
    if(len(hits)!=0):
        response=[]
        temp=[]
        for i in hits:
            temp.append(i["_source"])#This returns the actual MongoDb Document from course collection 

        for j in temp:
            response.append(j["name"])

        return response     #Returning the document deom the notes collection after searching.
    
    else:
        return []




ans=NGramSearch_Box("Ope")

if not ans:
    print("Not found, check the spelling...")

for i in ans:

    print(i)