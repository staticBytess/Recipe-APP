import requests
import json
import spoonacular as sp
import pprint 
from pymongo import MongoClient
from bson.objectid import ObjectId
import getpass
import re

client = MongoClient("mongodb://localhost:27017")

def addRecipe(username, data):
    client = MongoClient("mongodb://localhost:27017")
    db = client[username]
    collection = db["favorites"]

    ingredients_string = data["ingredients"]
    ingredients_list = eval(ingredients_string)
    data["ingredients"] = ingredients_list

    title = data["title"]
    recipe = {
        "_id":title,
        "data":data
    }
    collection.insert_one(recipe)

#Work in progress. Does not currently work
def updateRecipe(username, new, old = 0, _id = 0):
    db = client[username]
    collection = db["favorites"]

    if old == 0:
        delete(username, old)

     # Decode the JSON string back into a Python object
    ingredients_list = json.loads(new["ingredients"])
    new["ingredients"] = ingredients_list

    if _id == 0:
        title = new["title"]
    else:
        title = _id

    recipe = {
        "_id": title,
        "data": new
    }

    collection.insert_one(recipe)


def checkUser():

    userName = input("Username: ")
    password = getpass.getpass(prompt="Enter your password: ")

 
    with open('accounts.txt', 'r') as file:
        # Read the file line by line

        for line in file:
            if not line:
                break
            
            name, passkey = line.split()

            if userName == name and password==passkey:
                print("Account Found")
    return userName
                

def addUser():
    check = True
    while check != False:
        userName = input("Username: ")
        password = getpass.getpass(prompt="Enter your password: ")
        passwordCheck = getpass.getpass(prompt="Verify password: ")
        if password == passwordCheck:
            check = False
            with open('accounts.txt', 'a') as file:

                file.write(userName + " " + password+ "\n")
            client = MongoClient("mongodb://localhost:27017")
            db = client[userName]
            collection = db["favorites"]

        else:
            print("Passwords do not match, Try Again")
    



def saved(userName):

    db = client[userName]
    collection = db['favorites']

    documents = collection.find()
    recipeList = []
# Iterate over the documents and print the _id field of each document
    for document in documents:
        recipeList.append(document)
    
    return recipeList
        
def delete(userName, recipe):
    db = client[userName]
    collection = db['favorites']

    recDelete = re.compile(recipe, re.IGNORECASE)
    docDelete = collection.find_one({"_id": {"$regex": recDelete}})
    if docDelete:
        result = collection.delete_one({"_id": docDelete["_id"]})
        if result.deleted_count == 1:
            print("Document deleted successfully.")
        else:
            print("Document not found or could not be deleted.")
    else:
        print("Recipe not found try again")