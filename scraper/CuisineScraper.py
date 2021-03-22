from typing import Dict, List
from bs4 import BeautifulSoup
from .ICusineScraper import ICuisineScraper
from entities.cuisine_entity import Cuisine
import math


class CuisineScraper(ICuisineScraper):
    __TARGET_ID = "cuisines-collection"
    __TARGET_CLASS = "gel-layout gel-layout--equal promo-collection standard-12-promos"
    
    def scrape_cuisines(self, cuisines_page):
        cuisines_soup = BeautifulSoup(cuisines_page, "html.parser")
        results = cuisines_soup.find(id = self.__TARGET_ID).find(
            "div", class_ = self.__TARGET_CLASS)

        cuisines= [item["href"].split("/").pop() for item in results.find_all("a", href=True)]
        return cuisines
    
    def scrape_cuisine_metadata(self, cuisine_page: bytes, cuisine: str) -> Dict:
        cuisine_page_soup = BeautifulSoup(cuisine_page, "html.parser")
        total_results_count = cuisine_page_soup.find("div", class_ = "pagination-summary gel-wrap").find("b", class_="gel-pica-bold").text
        page_count = math.ceil(int(total_results_count)/24)
        
        return {
            cuisine : f"{total_results_count} recipes available",
            "pages" : page_count,
            "recipe_counts": total_results_count
        }
    