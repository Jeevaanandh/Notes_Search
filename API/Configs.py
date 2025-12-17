from pymongo import MongoClient
from elasticsearch import Elasticsearch


mongo= MongoClient("mongodb://localhost:27017/")
es= Elasticsearch("http://localhost:9200/")

db= mongo["Notes_Search"]
course= db["course"]
notes= db["notes"]