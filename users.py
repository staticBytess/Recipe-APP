import requests
import json
import spoonacular as sp
import pprint 
from pymongo import MongoClient
from bson.objectid import ObjectId
import getpass
from flask_bcrypt import Bcrypt


client = MongoClient('mongodb+srv://davidV:p6Vk8G8s!5g.23X@atlascluster.1m2wekf.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster')

def addRecipe(username, data, _id=0):
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


def checkUser(username, password):
    key =""
    passcheck = False
    #checks id username exists in database
    db_list = client.list_database_names()
    check = username in db_list
    if check:
        db = client[username]
        
        collection = db["password"]

        first_document = collection.find_one()
        key = first_document['_id']
        bcrypt = Bcrypt()
        passcheck = bcrypt.check_password_hash(key,password)

    if passcheck:
        return check
    else:
        check = False
        
    return check
                

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
    db = client[username]
    collection = db["favorites"]
    recipe_document = collection.find_one({"_id": recipe_title})
    if recipe_document:
        return recipe_document.get("data")
    else:
        return None
    
# Function to check if a document with the passed name exists in the database
def document_exists_for_date(name):
    db = client['recipeoftheday']
    collection = db['favorites']
    return collection.find_one({'_id': name}) is not None

