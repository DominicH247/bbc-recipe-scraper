from abc import ABC, abstractmethod
from typing import Dict, List

class IRecipeService(ABC):
    @abstractmethod
    async def get_dish_recipe(self) -> Dict:
        NotImplementedError
    
    @abstractmethod
    async def get_paths_for_recipes(self, page_number: int, cuisine_name: str) -> List:
        NotImplementedError
    
    @abstractmethod
    async def get_all_paths_for_recipes(self, total_pages: int, cuisine_name: str) -> List:
        NotImplementedError
    
    @abstractmethod
    async def get_recipe_details(self, path: str) -> Dict:
        NotImplementedError
    
    @abstractmethod
    async def get_recipe_details_async(self, path: str) -> Dict:
        NotImplementedError
    
    @abstractmethod
    async def get_all_recipe_details(self, recipe_paths: List) -> List:
        NotImplementedError