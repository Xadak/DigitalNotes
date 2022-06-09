import os
from pymongo import MongoClient
from flask import Flask
import initialize_data

mongodb_hostname = os.environ.get("MONGO_HOSTNAME", "localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

db = client["DigitalNotes"]

users = db["users"]

initialize_data.insert(users)
