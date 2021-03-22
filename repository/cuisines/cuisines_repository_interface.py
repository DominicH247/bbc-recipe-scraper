from abc import ABC, abstractmethod
from entities.cuisine_entity import Cuisine

class ICuisinesRepository(ABC):
    # @abstractmethod
    # async def set_collection(self) -> None:
    #     raise NotImplementedError
    
    @abstractmethod
    async def insert_item(cuisine: Cuisine) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def update_item(Cuisine: Cuisine) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_item(id: str) -> None:
        raise NotImplementedError