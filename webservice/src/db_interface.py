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
        deleted_user = self.users.find_one_and_delete(
            {"username": username_or_email})
        self.notes.delete_many({"user_id": deleted_user["_id"]})
        return deleted_user

    def add_note(self, user_id, title, date, content, tags):
        self.notes.insert_one(
            {"user_id": user_id, "title": title, "date": date, "content": content, "tags": tags})

    def edit_note(self, note_id,  user_id, title, date, content, tags):
        self.notes.replace_one({"_id": note_id},
                               {"user_id": user_id, "title": title, "date": date, "content": content, "tags": tags})

    def find_note_by_id(self, note_id):
        return self.notes.find_one({"_id": note_id})

    def notes_of(self, user_id):
        return self.notes.find({"user_id": user_id})

    def delete_note(self, user_id, note_id):
        return self.notes.find_one_and_delete({"user_id": user_id, "_id": note_id})
