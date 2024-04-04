import spoonacular as sp
import json
import requests
from bs4 import BeautifulSoup
from recipe import Recipe
from users import *


def remove_tags(html):
 
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
 
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
 
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

def parseData(data):
    
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
        return recipe
