import json


def insert(users):
    with open("./data/initial_admins.json", "r") as admin_file:
        admins = json.load(admin_file)
        for admin in admins:
            if users.find_one({"username": admin["username"]}) == None and users.find_one({"email": admin["email"]}) == None:
                users.insert_one(admin)
                print("admin inserted")
            else:
                print(admin["username"]+" already in databse")
