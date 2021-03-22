from abc import ABC, abstractmethod
from typing import Dict, List

class IRecipesBatchFetch(ABC):
    @abstractmethod
    async def get_all_recipe_details_batched(self, recipe_paths: List) -> List:
        pass