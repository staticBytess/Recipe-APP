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
from flask_bcrypt import Bcrypt


app = Flask(__name__)

bcrypt = Bcrypt()
api_key = "e3a3410195304ed7a410f3c4b6149a50"
client = MongoClient('mongodb+srv://davidV:p6Vk8G8s!5g.23X@atlascluster.1m2wekf.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster')

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
        if response.status_code == 404:
            error = "Recipe not found."
            return render_template("index.html", error=error)
        else:
            data = json.loads(response.text)
            recipe = parseData(data)

        return render_template("view.html", recipe = recipe, saved=0)
    
@app.route("/random")
def random():

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

    return render_template('view.html', recipe = recipe, saved=0, random=1)

    
@app.route("/recipeToday")
def recipeOfTheDay():

    username = 'recipeoftheday'
    db = client[username]  
    collection = db['favorites']
    current_date = datetime.now().date()

    if document_exists_for_date(str(current_date)):
        # If a document for the current date exists, fetch the recipe from the database
         recipe = getRecipe('recipeoftheday', str(current_date))
    else:
        collection.drop()
        api = sp.API(api_key)
        response = api.get_random_recipes()
        data = response.json()
        
        #random = ""
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
        ingredients_string = ' + '.join(recipe.ingredients)


        recipe_data = {
        "title": recipe.title,
        "id": recipe.id,
        "image": recipe.image,
        "summary": recipe.summary,
        "ingredients": ingredients_string,
        "website": recipe.website,
        "vegetarian": recipe.vegetarian,
        "vegan": recipe.vegan,
        "glutenFree": recipe.glutenFree,
        "instructions": recipe.instructions,
        }
        
        addRecipe("recipeoftheday", recipe_data, _id=str(current_date))

        recipe = getRecipe('recipeoftheday', str(current_date))
        
    return render_template('view.html', recipe=recipe, saved=0, homebtn=0)

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

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    
    return render_template("signup.html" )

@app.route("/createAccount", methods=['GET', 'POST'])
def createAccount():
    username = str(request.args.get('user_name'))
    password = str(request.args.get('password'))
    db_list = client.list_database_names()
    check = username in db_list
    if check == False:
        db = client[username]
        collection = db["password"]
    
        key = {
        "_id":bcrypt.generate_password_hash(password).decode('utf-8')
        }

        collection.insert_one(key)


    if check:
        return render_template('signup.html', error="Username already exits")


    return render_template("userdata.html", username = username)



@app.route("/userdata", methods=['GET'])
def userdata():


    username = str(request.args.get('user_name'))
    password = str(request.args.get('password'))

    
    

    if checkUser(username,password):
        recipeList = saved(username)
    else:
        return render_template('login.html', error="Username not found or Incorrect Password")


    return render_template("userdata.html", recipeList=recipeList, username = username)

@app.route("/delete", methods=['POST'])
def delete():
    username = request.form['username']
    recipe_id = request.form['recipe_id']
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
    password = request.form.get("password")

    
    if checkUser(username,password):
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
            "website": website,
            "vegetarian": vegetarian,  
            "vegan": vegan, 
            "glutenFree": glutenFree, 
            "summary": summary,
            "ingredients": ingredients,
            "instructions": instructions

        }
        db = client[username]
        collection = db["favorites"]

        existing_recipe = collection.find_one({"_id": title})
        if not existing_recipe:
            addRecipe(username, recipe_data)

        recipeList = saved(username) 

        return render_template("userdata.html", recipeList=recipeList, username = username)
    else:
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
        recipe = Recipe(title, id, image, summary,website, vegetarian,vegan, glutenFree, instructions, ingredients) 


        return render_template('addfave.html', recipe = recipe,error="Username not found or Incorrect Password")

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
        
    return render_template("view.html", recipe=recipe, saved=saved, username=username)

    
@app.route('/edit', methods=['GET'])
def display_data():
    username = request.args.get('username')
    recipe_id = request.args.get("recipe")  # Retrieve recipe ID from query parameters

    # Fetch the recipe data by its _id
    recipe = getRecipe(username, recipe_id)
    
    if recipe:
        return render_template('edit.html', recipe=recipe, username=username)
    else:
        return "Recipe not found."
    

@app.route('/updateRecipe', methods=['POST'])
def updateRecipe():

    username = str(request.form.get("username")) 
    recipe = str(request.form.get("original_title"))

    recipe_id = request.form.get("id")
    title = request.form.get("title")
    image = request.form.get("image")
    website = request.form.get("website")
    vegetarian = request.form.get("vegetarian")
    vegan = request.form.get("vegan")
    glutenFree = request.form.get("glutenFree")
    summary = request.form.get("summary")
    ingredients = request.form.get("ingredients")
    instructions = request.form.get("instructions")

    updated_recipe = {
        "title": title,
        "id": recipe_id,
        "image": image,
        "website": website,
        "vegetarian": vegetarian,  
        "vegan": vegan, 
        "glutenFree": glutenFree, 
        "summary": summary,
        "ingredients": ingredients,
        "instructions": instructions
    }

    db = client[username]
    collection = db['favorites']
    
    if(recipe == ""):
        collection.delete_one({"_id": updated_recipe["title"]})
    else:
        collection.delete_one({"_id": recipe})

    addRecipe(username, updated_recipe)

    recipeList = saved(username)

    return render_template("userdata.html", recipeList=recipeList, username = username)

@app.route('/createNewRecipe', methods=['POST'])
def createNewRecipe():
    username = str(request.form.get("username")) 
    recipe = {
        "title": "",
        "id": "",
        "image": "",
        "website": "",
        "vegetarian": "",  
        "vegan": "", 
        "glutenFree": "", 
        "summary": "",
        "ingredients": "",
        "instructions": ""
    }
    return render_template("edit.html", username=username, recipe=recipe)


if __name__ == '__main__':
    app.run(debug=True, port=5001)



