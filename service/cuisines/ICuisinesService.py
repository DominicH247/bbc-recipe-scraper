from abc import ABC, abstractmethod
from typing import Dict, List

class ICuisineService(ABC):
    @abstractmethod
    async def get_available_cuisines(self) -> List:
        pass
    
    async def get_cuisine_meta_data(self) -> Dict:
        pass