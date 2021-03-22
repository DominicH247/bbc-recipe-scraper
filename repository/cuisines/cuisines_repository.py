from .cuisines_repository_interface import ICuisinesRepository
from typing import Dict 
from context.client_interface import IClientInterface
from schemas.cuisine_schema import cuisine_schema
from entities.cuisine_entity import Cuisine

class CuisinesRepositoryMongoDb(ICuisinesRepository):
    _data_base = "recipes_db"
    _collection = "cuisines"
    
    def __init__(self, client: IClientInterface):
        self._client = client
        
    async def insert_item(self, cuisine: Cuisine) -> str:
        """
        Asynchronously insert a cuisine document into mongoDB only if cuisine does not already exist
        """
        query = {
            "name": cuisine.get_name()
        }
        
        isExisting  = True if await self._client[self._collection].count_documents(query) > 0 else False

        if isExisting == False:
            try:
                stored = await self._client[self._collection].insert_one(cuisine.get_cuisine())
                return stored.inserted_id
            except Exception as err:
                print(err)
        
    async def update_item(self, cuisine_id: str, recipe_id: str) -> None:
        """
        updates item
        """
        await self._client[self._collection].update_one({"_id": cuisine_id}, {"$push": {"recipes": str(recipe_id)}})

    async def delete_item(self, id: str) -> None:
        """
        Asynchronously delete the cuisine by its ID and associated recipes in an ACID transaction
        """
        pass