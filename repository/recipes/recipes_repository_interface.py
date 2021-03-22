from abc import ABC, abstractmethod
from entities.recipe_entity import Recipe

class IRecipesRepository(ABC):    
    @abstractmethod
    async def insert_item(recipe: Recipe) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def fetch_recipe_by_id(self, recipe_id: str) -> Recipe:
        raise NotImplementedError
    
    @abstractmethod
    async def update_item(recipe: Recipe) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_item(id: str) -> None:
        raise NotImplementedError