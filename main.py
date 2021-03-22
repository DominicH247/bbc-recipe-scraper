import random
import asyncio
from repository.recipes.recipes_repository import RecipesRepositoryMongoDb
from service.cuisines.CuisineService import CuisineService
from service.recipes.RecipeService import RecipeService
from scraper.CuisineScraper import CuisineScraper
from scraper.RecipeScraper import RecipeScraper
from repository.cuisines.cuisines_repository import CuisinesRepositoryMongoDb
from schemas.cuisine_schema import cuisine_schema
from schemas.recipe_schema import recipe_schema
from context.mongodb_client import MongoClient

async def initiate(cuisine_name: str, cuisine_service: CuisineService, recipe_service: RecipeService): 
    # CUSINES
    cuisine_meta_data = await cuisine_service.get_cuisine_meta_data(cuisine_name)
            
    # RECIPES
    all_paths = await recipe_service.get_all_paths_for_recipes(cuisine_meta_data["pages"], cuisine_name)
    if(len(all_paths) < 500):
        return await recipe_service.get_all_recipe_details(all_paths, cuisine_meta_data["cuisine_id"])
    else:
        return await recipe_service.get_all_recipe_details_batched(all_paths)
        

async def main():
    client = await MongoClient().get_connection(
        "recipes_db", 
        {
            "cuisines_collection": "cuisines",
            "recipes_collection": "recipes",
            "cuisine_schema": cuisine_schema,
            "recipe_schema": recipe_schema
        }
    )

    cuisine_scraper = CuisineScraper()
    cuisine_repo = CuisinesRepositoryMongoDb(client)
    cuisine_service = CuisineService(cuisine_scraper, cuisine_repo)
    
    recipe_scraper = RecipeScraper()
    recipe_repo = RecipesRepositoryMongoDb(client)
    recipe_service = RecipeService(recipe_scraper, recipe_repo, cuisine_repo)
    
    available_cuisines = await cuisine_service.get_available_cuisines()
    
    recipes = []
    
    throttle = random.randint(1,15)
    for cuisine in available_cuisines:

        recipes.append(await asyncio.create_task(initiate(
            cuisine, 
            cuisine_service,
            recipe_service
        )))
        await asyncio.sleep(throttle)

asyncio.run(main())
