from abc import ABC, abstractmethod
from typing import List
from entities.recipe_entity import Recipe

class IRecipeScraper(ABC):
    @abstractmethod
    def scrape_recipe_path(self, recipes_page: bytes) -> List:
        NotImplementedError
    
    @abstractmethod
    def scrape_recipe_details(self, path: str) -> Recipe:
        NotImplementedError
