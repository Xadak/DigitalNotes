import os
from pymongo import MongoClient


class DBHandle:
    def __init__(self):
        mongodb_hostname = os.environ.get("MONGO_HOSTNAME", "localhost")
        client = MongoClient('mongodb://'+mongodb_hostname+':27017/')
        db = client["DigitalNotes"]

        self.users = db["users"]
        self.notes = db["notes"]

    def find_user(self, username_or_email, password):
        return self.users.find_one({"$or": [{"username": username_or_email}, {"email": username_or_email}], "password": password})

    def delete_user(self, username_or_email):
        return self.users.find_one_and_delete({"username": username_or_email})
