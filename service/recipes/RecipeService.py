from .IRecipesService import IRecipeService
from .IRecipesBatchFetch import IRecipesBatchFetch
from scraper.IRecipeScraper import IRecipeScraper
from repository.recipes.recipes_repository_interface import IRecipesRepository
from repository.cuisines.cuisines_repository_interface import ICuisinesRepository
from settings import Settings
from typing import Dict, List
from entities.recipe_entity import Recipe
import asyncio
import requests
import math
import random
from aiohttp.client import ClientSession


class RecipeService(IRecipeService, IRecipesBatchFetch):
    
    def __init__(self, RecipeScraper: IRecipeScraper, recipe_repo: IRecipesRepository, cuisine_repo: ICuisinesRepository) -> None:
        self._recipe_scraper = RecipeScraper
        self._recipe_repo = recipe_repo
        self._cuisine_repo = cuisine_repo
    
    async def get_dish_recipe(self) -> Dict:
        pass
    
    async def get_paths_for_recipes_async(self, page_num: int, cuisine_name: str) -> List:
        async with ClientSession() as session:
            async with session.get(f"{Settings._BASE_URL}{Settings._SEARCH_PATH}?cuisines={cuisine_name}&page={page_num}") as response:
                recipes_page = await response.read()
                return await self._recipe_scraper.scrape_recipe_path(recipes_page)
        
    async def get_paths_for_recipes(self, page_num: int, cuisine_name: str) -> List:
        recipes_page = requests.get(f"{Settings._BASE_URL}{Settings._SEARCH_PATH}?cuisines={cuisine_name}&page={page_num}")
        return await self._recipe_scraper.scrape_recipe_path(recipes_page.content)
    
    async def get_all_paths_for_recipes(self, total_pages: int, cuisine_name: str) -> List:
        all_paths = []
        if(total_pages < 10):
            all_paths = await asyncio.gather(*[self.get_paths_for_recipes_async(page, cuisine_name) for page in range(1, total_pages + 1)])
        else:
            all_paths = await asyncio.gather(*[self.get_paths_for_recipes(page, cuisine_name) for page in range(1, total_pages + 1)])
            
        # flatten array move into seperate func
        return [item for sublist in all_paths for item in sublist]
    
    async def get_recipe_details(self, path: str, cuisine_id: str) -> bytes:
        recipe_page = requests.get(f"https://www.bbc.co.uk{path}")
        recipe_entity = await self._recipe_scraper.scrape_recipe_details(recipe_page.content)
        # store in db
        
        inserted_id = await self._recipe_repo.insert_item(recipe_entity)
        
        # update cuisine with newly inserted recipe id
        await self._cuisine_repo.update_item(cuisine_id, inserted_id)
        
        return recipe_entity
        
    async def get_recipe_details_async(self, path: str, cuisine_id: str) -> bytes:
        async with ClientSession() as session:
            async with session.get(f"https://www.bbc.co.uk{path}") as response:
                recipe_page = await response.read()
                recipe_entity = await self._recipe_scraper.scrape_recipe_details(recipe_page)
                
                inserted_id = await self._recipe_repo.insert_item(recipe_entity)
                
                # update cuisine with newly inserted recipe id
                await self._cuisine_repo.update_item(cuisine_id, inserted_id)
                
                return recipe_entity
    
    async def get_all_recipe_details(self, recipe_paths: List, cuisine_id: str) -> List:
        if(len(recipe_paths) <= 30):
            return await asyncio.gather(*[self.get_recipe_details_async(path, cuisine_id) for path in recipe_paths])
        else:
            return await asyncio.gather(*[self.get_recipe_details(path, cuisine_id) for path in recipe_paths])
            
    async def get_all_recipe_details_batched(self, recipe_paths: List ) -> List:
        # Batch process
        batch_size = 200
        throttle = 5
        steps = math.ceil(len(recipe_paths) / batch_size)
        start_idx = 0
        end_idx = batch_size
        recipes_details = []
        
        while steps > 0:
            batched_paths = recipe_paths[start_idx : end_idx]
            batched_recipes = await asyncio.gather(*[self.get_recipe_details(path) for path in batched_paths])
            recipes_details += batched_recipes
            start_idx += batch_size
            end_idx += batch_size
            steps -= 1
            await asyncio.sleep(throttle)
                
        return recipes_details