from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['github_events']
collection = db['events']

def insert_event(event_type, author, from_branch, to_branch):
    event = {
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "type": event_type,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(event)

def get_latest_events(limit=10):
    return list(collection.find().sort("timestamp", -1).limit(limit))
