from scraper.IRecipeScraper import IRecipeScraper
from entities.recipe_entity import Recipe
from typing import Dict, List
from bs4 import BeautifulSoup

class RecipeScraper(IRecipeScraper):
    _TARGET_CONTAINER = "gel-layout gel-layout--equal promo-collection"
    _TARGET_ITEM = "gel-layout__item gel-1/2 gel-1/4@xl"
    
    async def scrape_recipe_path(self, recipes_page: bytes) -> List:
        recipes_soup = BeautifulSoup(recipes_page, "html.parser")
        recipes_paths = [item.find("a", href=True)["href"] for 
                item in recipes_soup.find("div", class_=self._TARGET_CONTAINER).find_all("div", class_=self._TARGET_ITEM)]
        return recipes_paths
    
    async def scrape_recipe_details(self, recipe_page: bytes) -> Recipe:
        recipe_soup = BeautifulSoup(recipe_page, "html.parser")
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

        # retrurn recipe entity
        return Recipe(title, prep_time, cook_time, dietry, ingredients_formatted, method)
        