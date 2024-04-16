import requests
import json
import spoonacular as sp
import pprint 
from pymongo import MongoClient
from bson.objectid import ObjectId
import getpass
import re

client = MongoClient("mongodb://localhost:27017")

def addRecipe(username, data, _id=0):
    client = MongoClient("mongodb://localhost:27017")
    db = client[username]
    collection = db["favorites"]

    ingredients_string = data["ingredients"]
    # Remove brackets
    ingredients_string = ingredients_string.replace("[", "").replace("]", "")
    # Split the string by comma and then remove opening/closing apostrophes
    ingredients_list = [ingredient.strip("'") for ingredient in ingredients_string.split("', '")]

    # Update data with cleaned ingredients list
    data["ingredients"] = ingredients_list

    if _id==0:
        title = data["title"]
        recipe = {
            "_id":title,
            "data":data
        }
    else:
        recipe = {
            "_id":_id,
            "data":data
        }
    collection.insert_one(recipe)

#Work in progress. Does not currently work
# def updateRecipe(username, recipe, _id = 0):
#     db = client[username]
#     collection = db["favorites"]
#     delete(username, recipe)

#      # Decode the JSON string back into a Python object
#     ingredients_list = json.loads(recipe["ingredients"])
#     recipe["ingredients"] = ingredients_list

#     if _id == 0:
#         title = recipe["title"]
#     else:
#         title = _id

#     recipe = {
#         "_id": title,
#         "data": recipe
#     }

#     collection.insert_one(recipe)


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
        
def delete_recipe(username, recipe_title):
    client = MongoClient("mongodb://localhost:27017")
    db = client[username]
    collection = db['favorites']

    result = collection.delete_one({"_id": recipe_title})
    
    if result.deleted_count == 1:
        print("Deleted")
    else:
        print("Document not found")

def delete_collection(username, collection):
    db = client[username]
    collection = db['favorites']
    
    # Delete the collection
    collection.drop()
    
    return 'Collection deleted successfully!'

def getRecipe(username, recipe_title):
    client = MongoClient("mongodb://localhost:27017")
    db = client[username]
    collection = db["favorites"]
    recipe_document = collection.find_one({"_id": recipe_title})
    if recipe_document:
        return recipe_document.get("data")
    else:
        return None
    
# Function to check if a document with the passed name exists in the database
def document_exists_for_date(name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['recipeoftheday']
    collection = db['favorites']
    return collection.find_one({'_id': name}) is not None