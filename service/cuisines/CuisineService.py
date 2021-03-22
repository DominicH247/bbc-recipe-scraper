from typing import List, Dict
from settings import Settings
from scraper.CuisineScraper import ICuisineScraper
from .ICuisinesService import ICuisineService
from entities.cuisine_entity import Cuisine
from repository.cuisines.cuisines_repository_interface import ICuisinesRepository

from aiohttp.client import ClientSession

class CuisineService(ICuisineService):
    def __init__(self, CuisineScraper: ICuisineScraper, cuisine_repo: ICuisinesRepository):
        self._cuisine_scraper = CuisineScraper
        self._cuisine_repo = cuisine_repo
    
    async def get_available_cuisines(self) -> List:
        try:
            async with ClientSession() as session:
                async with session.get(f"{Settings._BASE_URL}{Settings._CUISINES_PATH}") as response:
                    cuisines_page = await response.read()
        except Exception as error:
            print(error)
        else:
            return self._cuisine_scraper.scrape_cuisines(cuisines_page)
    
    async def get_cuisine_meta_data(self, cuisine_name: str) -> Dict:
        try:
            async with ClientSession() as session:
                async with session.get(f"{Settings._BASE_URL}{Settings._SEARCH_PATH}?&cuisines={cuisine_name}") as response:
                    cuisine_page = await response.read()
        except Exception as error:
            print(error)
        else:            
            cuisine_data = self._cuisine_scraper.scrape_cuisine_metadata(cuisine_page, cuisine_name)
            
            cuisine_entity = Cuisine(cuisine_name, cuisine_data["recipe_counts"])
    
            inserted_id = await self._cuisine_repo.insert_item(cuisine_entity)
            print(inserted_id)
            # get stored cuisine id and add to cuisine dict
            cuisine_data["cuisine_id"] = inserted_id
            return cuisine_data
