import os
from pymongo import MongoClient


class DBHandle:
    def __init__(self):
        mongodb_hostname = os.environ.get("MONGO_HOSTNAME", "localhost")
        client = MongoClient('mongodb://'+mongodb_hostname+':27017/')
        db = client["DigitalNotes"]

        self.users = db["users"]
        self.notes = db["notes"]

    def find_user_by_username(self, username, password):
        return self.users.find_one({"username": username, "password": password})
