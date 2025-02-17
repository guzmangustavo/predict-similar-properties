import redis

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


mongo_client = MongoClient('mongodb://mongo:27017/')
mongo_db = mongo_client.prediction_microservices
subscription_collection = mongo_db.subscriptions

redis_client = redis.Redis(host='redis', port=6379, db=0)


def get_subscription_by_api_key(api_key):
    api_key_data = subscription_collection.find_one({"api_key": api_key})
    return api_key_data if api_key_data else None


def insert_api_key(api_key):
    try:
        subscription_collection.insert_one(api_key)
        return True

    except DuplicateKeyError:
        return False

    except Exception as e:
        return False
