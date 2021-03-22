from abc import ABC, abstractmethod
from typing import Dict, List

class ICuisineScraper(ABC):
    @abstractmethod
    def scrape_cuisines(self, cuisines_page: bytes) -> List:
        pass
    
    def scrape_cuisine_metadata(self, cuisine_page: bytes, cuisine: str ) -> Dict:
        pass