from flask import Flask, render_template, request
import spoonacular as sp
import json
import requests
from bs4 import BeautifulSoup
from recipe import Recipe

def remove_tags(html):
 
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
 
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
 
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

app = Flask(__name__)

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
                    "apiKey":"dc50e9f7e4004f78a7f58d800ead2fe3",
                    
                }
        response = requests.get(url, params)
        data = json.loads(response.text)

        id = data["id"]
        image = data['image']
        title = data["title"]
        summary = remove_tags(data["summary"])
        website = data['sourceUrl']
        vegetarian = data['vegetarian']
        vegan = data['vegan']
        glutenFree = data['glutenFree']
        image = data['image']
        instructions = remove_tags(data['instructions'])


        instruc = data['extendedIngredients']
        ingredients=[]
        for inst in instruc:
            ingredients.append(inst['original'])

        recipe = Recipe(title,id,image, summary,website,vegetarian,vegan,glutenFree,instructions,ingredients)
        return render_template("id.html", recipe = recipe)
    
@app.route("/random")
def random():

    api = sp.API("dc50e9f7e4004f78a7f58d800ead2fe3")

    response = api.get_random_recipes()
        
    data = response.json()
    
    random = ""
    recepies = data['recipes'] 
    for recepieTitle in recepies:
        random = str(recepieTitle["id"])
    url = "https://api.spoonacular.com/recipes/" + random + "/information"
    params = {
                "apiKey":"dc50e9f7e4004f78a7f58d800ead2fe3",
                
             }
    response = requests.get(url, params)
    data = json.loads(response.text)

    id = data["id"]
    image = data['image']
    title = data["title"]
    summary = remove_tags(data["summary"])
    website = data['sourceUrl']
    vegetarian = data['vegetarian']
    vegan = data['vegan']
    glutenFree = data['glutenFree']
    image = data['image']
    instructions = remove_tags(data['instructions'])


    instruc = data['extendedIngredients']
    ingredients=[]
    for inst in instruc:
        ingredients.append(inst['original'])


    recipe = Recipe(title,id,image, summary,website,vegetarian,vegan,glutenFree,instructions,ingredients)

    return render_template('random.html', recipe = recipe)

@app.route("/idInfo", methods = ['GET', 'POST'])
def idInfo():
    
        
        value = request.args.get('value')
        
        url = f"https://api.spoonacular.com/recipes/"+value+"/information"
        params = {
                    "apiKey":"dc50e9f7e4004f78a7f58d800ead2fe3",
                    
                }
        response = requests.get(url, params)
        data = json.loads(response.text)

        id = data["id"]
        image = data['image']
        title = data["title"]
        summary = remove_tags(data["summary"])
        website = data['sourceUrl']
        vegetarian = data['vegetarian']
        vegan = data['vegan']
        glutenFree = data['glutenFree']
        image = data['image']
        instructions = remove_tags(data['instructions'])


        instruc = data['extendedIngredients']
        ingredients=[]
        for inst in instruc:
            ingredients.append(inst['original'])

        recipe = Recipe(title,id,image, summary,website,vegetarian,vegan,glutenFree,instructions,ingredients)
        return render_template("idInfo.html", recipe = recipe)

@app.route("/searchResults", methods=['GET', 'POST'])
def search():


    if request.method == 'POST':
        selection = str(request.form['search_criteria'])
        
        search = str(request.form['search_query'])
        if selection == "ingredient":
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
                        "apiKey":"dc50e9f7e4004f78a7f58d800ead2fe3",
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
                    "apiKey":"dc50e9f7e4004f78a7f58d800ead2fe3",
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
            "apiKey":"dc50e9f7e4004f78a7f58d800ead2fe3",
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



if __name__ == '__main__':
    app.run(debug=True, port=5001)




