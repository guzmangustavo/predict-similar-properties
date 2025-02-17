from pymongo import MongoClient


client = MongoClient('mongodb://mongo:27017/')
db = client.prediction_microservices
logs_collection = db.logs