from flask import Flask, render_template, request, redirect
import spoonacular as sp
import json
import requests
from bs4 import BeautifulSoup
from recipe import Recipe
from users import *
from methods import *
import time
from datetime import datetime


app = Flask(__name__)

api_key = "9864ec4977cf4c629b1b4a5647a9e502"

@app.route("/")
@app.route("/home")


def home():
    return render_template("index.html")

@app.route("/id", methods=['GET', 'POST'])
def id():
    if request.method == 'POST':
        
        data_input = str(request.form['data_input'])
        
        url = f"https://api.spoonacular.com/recipes/"+data_input+"/information"
        params = {
                    "apiKey":api_key,
                    
                }
        response = requests.get(url, params)
        data = json.loads(response.text)
        recipe = parseData(data)

        return render_template("id.html", recipe = recipe)
    
@app.route("/random")
def random():

    api = sp.API(api_key)

    #response = api.get_random_recipes()
        
    #data = response.json()
    
    random = "782585"
    recepies = data['recipes'] 
    for recepieTitle in recepies:
        random = str(recepieTitle["id"])
    url = "https://api.spoonacular.com/recipes/" + random + "/information"
    params = {
                "apiKey":api_key,
                
             }
    response = requests.get(url, params)
    data = json.loads(response.text)
    recipe = parseData(data)
    return render_template('random.html', recipe = recipe)

# Function to check if a document with the current date exists in the database
def document_exists_for_date(date):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['recipeoftheday']
    collection = db['favorites']
    return collection.find_one({'_id': date}) is not None

#does not currently work. Needs to be able to update a document
@app.route("/recipeToday")
def recipeOfTheDay():

    client = MongoClient('mongodb://localhost:27017/')
    db = client['recipeoftheday']  
    collection = db['favorites']

    current_date = datetime.now().date()

    if document_exists_for_date(str(current_date)):
        # If a document for the current date exists, fetch the recipe from the database
        recipe = collection.find_one({'_id': str(current_date)})
    else:
        api = sp.API(api_key)
        response = api.get_random_recipes()
        data = response.json()
        
        random = ""
        recepies = data['recipes'] 
        for recepieTitle in recepies:
            random = str(recepieTitle["id"])
        url = "https://api.spoonacular.com/recipes/" + random + "/information"
        params = {
                    "apiKey":api_key,
                    
                }
        response = requests.get(url, params)
        data = json.loads(response.text)
        recipe = parseData(data)

        recipe_data = {
        "title": recipe.title,
        "id": recipe.id,
        "image": recipe.image,
        "summary": recipe.summary,
        "ingredients": json.dumps(recipe.ingredients),
        "website": recipe.website,
        "vegetarian": recipe.vegetarian,
        "vegan": recipe.vegan,
        "glutenFree": recipe.glutenFree,
        "instructions": recipe.instructions,
        }
        addRecipe("recipeoftheday", recipe_data)
        
        document = collection.find_one({'_id': recipe.title})  # Assuming you're updating this document

        if document:
            # Update the _id field
            updateRecipe("recipeoftheday", recipe_data, recipe_data, _id = str(current_date))
            print("Document updated successfully.")
        else:
            print("Document not found.")

        recipe = getRecipe('recipeoftheday', recipe.title)
        
    return render_template('random.html', recipe=recipe)

# @app.route("/idInfo", methods = ['GET', 'POST'])
# def idInfo():
    
        
#         value = request.args.get('value')
        
#         url = f"https://api.spoonacular.com/recipes/"+value+"/information"
#         params = {
#                     "apiKey":"b67eb3c9d9f94a94bc7d8d966daa48fc",
                    
#                 }
#         response = requests.get(url, params)
#         data = json.loads(response.text)

#         recipe = parseData(data)
#         return render_template("idInfo.html", recipe = recipe)

@app.route("/searchResults", methods=['GET', 'POST'])
def search():


    if request.method == 'POST':
        selection = str(request.form['search_criteria'])
        
        search = str(request.form['search_query'])
        if selection == "ingredient":
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
                        "apiKey":api_key,
                        "query":search
                    }

            response = requests.get(url, params)
            data = json.loads(response.text)
            recipes = data['results']

            recipeList = []


            for recepieTitle in recipes:
                id = recepieTitle['id']
                title = recepieTitle['title']
                image = recepieTitle['image']
                recipe = Recipe(title,id,image)
                recipeList.append(recipe)


            return render_template('searchResults.html', recipeList = recipeList, selection=selection)
        elif selection == "cuisine":
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
                    "apiKey":api_key,
                    "cuisine":search,
                    "number":10
                      }
            response = requests.get(url, params=params)
            data = json.loads(response.text)
            recipes = data['results'] 
            recipeList = []


            for recepieTitle in recipes:
                id = recepieTitle['id']
                title = recepieTitle['title']
                image = recepieTitle['image']
                recipe = Recipe(title,id,image)
                recipeList.append(recipe)


            return render_template('searchResults.html', recipeList = recipeList, selection=selection)
        elif selection == "diet":
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
            "apiKey":api_key,
            "diet":search,
            "number":10
            }
            response = requests.get(url, params)
            data = json.loads(response.text)
            recipes = data['results'] 
            recipeList = []


            for recepieTitle in recipes:
                id = recepieTitle['id']
                title = recepieTitle['title']
                image = recepieTitle['image']
                recipe = Recipe(title,id,image)
                recipeList.append(recipe)


            return render_template('searchResults.html', recipeList = recipeList, selection=selection)

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    return render_template("login.html" )

@app.route("/userdata", methods=['GET', 'POST'])
def userdata():
    username = str(request.form['user_name'])
    password = str(request.form['password'])

    recipeList = saved(username) 

    return render_template("userdata.html", recipeList=recipeList, username = username)

@app.route("/delete", methods=['POST'])
def delete():
    username = request.form['username']
    recipe_id = request.form['recipe_id']
    
    client = MongoClient("mongodb://localhost:27017")
    db = client[username]
    collection = db['favorites']

    collection.delete_one({"_id": recipe_id})

    recipeList = saved(username)

    return render_template("userdata.html", recipeList = recipeList, username = username)

@app.route("/addFave", methods=['GET', 'POST'])
def addFave():
    value = request.args.get('value')
    url = f"https://api.spoonacular.com/recipes/"+value+"/information"

    params = {
                "apiKey":"b67eb3c9d9f94a94bc7d8d966daa48fc",

            }
    
    response = requests.get(url, params)
    data = json.loads(response.text)
    recipe = parseData(data)

    return render_template("addfave.html", recipe = recipe)

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    username = request.form.get("user_name")

    #This can probably be simplified so we do not have get each individual field
    title = request.form.get("title")
    id = request.form.get("id")
    image = request.form.get("image")
    summary = request.form.get("summary")
    image = request.form.get("image")
    ingredients = request.form.get("ingredients")
    website = request.form.get("website")
    vegetarian= request.form.get("vegetarian")
    vegan= request.form.get("vegan")
    glutenFree= request.form.get("glutenFree")
    instructions= request.form.get("instructions")

    # Creates a dictionary representing the recipe data
    recipe_data = {
        "title": title,
        "id": id,
        "image": image,
        "summary": summary,
        "ingredients": ingredients,
        "website": website,
        "vegetarian": vegetarian,
        "vegan": vegan,
        "glutenFree": glutenFree,
        "instructions": instructions,

    }

    addRecipe(username, recipe_data)

    return "Recipe added successfully!"

@app.route("/view", methods=['POST', 'GET'])
def view():
    
    username = request.args.get("username") 
    
    if request.method == 'GET': #if called from userdata.html
        recipe = request.args.get("recipe")
        recipe = getRecipe(username, recipe)
        saved = 1
    else: #if called from any other html
        recipe = request.form.get('value')
        recipe = str(recipe)
        url = f"https://api.spoonacular.com/recipes/"+recipe+"/information"
        params = {
                    "apiKey":"b67eb3c9d9f94a94bc7d8d966daa48fc",
                    
                }
        response = requests.get(url, params)
        data = json.loads(response.text)

        recipe = parseData(data)
        saved = 0
        
    return render_template("view.html", recipe=recipe, saved=saved)

def getRecipe(username, recipe_title):
    client = MongoClient("mongodb://localhost:27017")
    db = client[username]
    collection = db["favorites"]
    recipe_document = collection.find_one({"_id": recipe_title})
    if recipe_document:
        return recipe_document.get("data")
    else:
        return None
    
@app.route('/edit', methods=['GET'])
def display_data():
    username = request.args.get('username')
    recipe_id = request.args.get("recipe")  # Retrieve recipe ID from query parameters

    # Fetch the recipe data by its _id
    recipe = getRecipe(username, recipe_id)
    
    if recipe:
        return render_template('edit.html', recipe=recipe)
    else:
        return "Recipe not found."

if __name__ == '__main__':
    app.run(debug=True, port=5001)