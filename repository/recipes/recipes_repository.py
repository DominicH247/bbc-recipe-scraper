from .recipes_repository_interface import IRecipesRepository
from entities .recipe_entity import Recipe
from context.client_interface import IClientInterface
from schemas.recipe_schema import recipe_schema
from entities.recipe_entity import Recipe

class RecipesRepositoryMongoDb(IRecipesRepository):
    _data_base = "recipes_db"
    _collection = "recipes"
    
    
    def __init__(self,  client: IClientInterface):
        self._client = client
    
    async def insert_item(self, recip_entity: Recipe) -> None:

        query = {
            "name": recip_entity.get_name()
        }

        isExisting  = True if await self._client[self._collection].count_documents(query) > 0 else False
        
        if isExisting == False:
            try:
                stored = await self._client[self._collection].insert_one(recip_entity.get_recipe())
                return stored.inserted_id
                
            except Exception as err:
                print(err, end=" ERRR")
                
    
    async def fetch_recipe_by_id(self, recipe_id: str) -> Recipe:
        """
        Fetches recipe by its id
        """
        return await self._client[self._collection].query({"id": recipe_id})
    
    async def update_item(recipe: Recipe) -> None:
        return super().update_item()
    
    async def delete_item(id: str) -> None:
        return super().delete_item()
    