from aiohttp.client import ClientSession
import requests
from bs4 import BeautifulSoup
import asyncio
import math


BASE_URL = "https://www.bbc.co.uk/food"
CUISINES_PATH = "/cuisines"
SEARCH_PATH= "/search"
RECIPES_PATH = "/recipes"


TARGET_ID = "cuisines-collection"
TARGET_CLASS = "gel-layout gel-layout--equal promo-collection standard-12-promos"

# get array of available cuisnes
async def get_cuisines(session):
    async with session.get(f"{BASE_URL}{CUISINES_PATH}") as response:
        cuisines_page = await response.read()
        cuisines_soup = BeautifulSoup(cuisines_page, "html.parser")
        results = cuisines_soup.find(id = TARGET_ID).find(
            "div", class_ = TARGET_CLASS)

        cuisines= [item["href"].split("/").pop() for item in results.find_all("a", href=True)]
        return cuisines

async def cuisine_pages(cuisine, session):
    async with session.get(f"{BASE_URL}{SEARCH_PATH}?&cuisines={cuisine}") as response:
        cuisine_page = await response.read()
        cuisine_page_soup = BeautifulSoup(cuisine_page, "html.parser")
        total_results_count = cuisine_page_soup.find("div", class_ = "pagination-summary gel-wrap").find("b", class_="gel-pica-bold").text
        page_count = math.ceil(int(total_results_count)/24)
        return {
            cuisine : total_results_count,
            "pages" : page_count
        }

# get reipes
async def fetch_recipe_paths(cuisine, page_num, session):
    async with session.get(f"{BASE_URL}{SEARCH_PATH}?cuisines={cuisine}&page={page_num}") as response:
        recipes_page = await response.read()
        recipes_soup = BeautifulSoup(recipes_page, "html.parser")
        recipes_paths = [item.find("a", href=True)["href"] for 
            item in recipes_soup.find("div", class_="gel-layout gel-layout--equal promo-collection").find_all("div", class_="gel-layout__item gel-1/2 gel-1/4@xl")]
        return recipes_paths

# get all recipe paths
async def fetch_all_recipe_paths(cuisine, pages_data, session):
    print(f"Analyzing available recipes for {cuisine} food...")
    paths = await asyncio.gather(*[fetch_recipe_paths(cuisine, page, session) for page in range(1, pages_data['pages'] + 1)])
    return flatten_paths(paths)


def flatten_paths(array):
    print("Processing paths...")
    return [item for sublist in array for item in sublist]


# get all recipes
async def fetch_all_recipe_details(recipes, session):
    print("Fetching recipes...")
    return await asyncio.gather(*[fetch_recipe_detail(recipe_path, session) for recipe_path in recipes])

# get each recipe in the array
async def fetch_recipe_detail(recipe_path, session) -> None:
    """
    website limits number of parallel requests 
    async with session.get(f"https://www.bbc.co.uk{recipe_path}") as response:
    """
    recipe_page = requests.get(f"https://www.bbc.co.uk{recipe_path}")
    recipe_soup = BeautifulSoup(recipe_page.content, "html.parser")
    results = recipe_soup.find("div", class_="recipe-main-info gel-layout__item gel-1/1 gel-2/3@l")
    
    title = results.find("h1", class_="gel-trafalgar content-title__text").text
    
    dietry = results.find("p", class_="recipe-metadata__dietary-vegetarian-text").text if results.find("p", class_="recipe-metadata__dietary-vegetarian-text") != None else None
    prep_time = results.find("p", class_="recipe-metadata__prep-time").text
    cook_time = results.find("p", class_="recipe-metadata__cook-time").text
    method = [method.text for method in results.find("ol", class_="recipe-method__list").find_all("li", class_="recipe-method__list-item")]
    
    # some ingredients have sub sections
    lists = results.find_all("ul", class_="recipe-ingredients__list")
    ingredients_all = [ingredient.find_all("li", class_="recipe-ingredients__list-item") for ingredient in lists]
    ingredients_all_flat = [item for sublist in ingredients_all for item in sublist]
    ingredients_formatted = [ingredient.text for ingredient in ingredients_all_flat]
    
    return {
        "title" : title,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "dietry" : dietry,
        "ingredients": ingredients_formatted,
        "method": method
    }
    
async def generate_recipes(cuisine, session):
    pages_data = await cuisine_pages(cuisine, session)
    recipes_paths = await fetch_all_recipe_paths(cuisine, pages_data, session)
    return await fetch_all_recipe_details(recipes_paths, session)
    
    
async def async_main():
    async with ClientSession() as session:        
        cuisines = await get_cuisines(session)
        # recipes = await asyncio.gather(*[generate_recipes(cuisine, session) for cuisine in cuisines])
        recipes_task = await asyncio.gather(generate_recipes("african", session))
        print(flatten_paths(recipes_task))
    
asyncio.run(async_main())

