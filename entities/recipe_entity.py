from typing import List, Dict

class Recipe:
    def __init__(
        self, 
        name: str="", 
        prep_time: str="", 
        cook_time: str="", 
        dietry: str=None, 
        ingredients: List=[], 
        method: List=[]) -> None:
        self._name = name
        self._rating = 0
        self._prep_time = prep_time
        self._cook_time = cook_time
        self._dietry = dietry
        self._ingredients = ingredients
        self._method = method

    def get_name(self) -> str:
        return self._name
    
    def set_name(self, name: str) -> None:
        self._name = name
    
    def get_rating(self) -> str:
        return self._rating
    
    def set_rating(self, rating: str) -> None:
        self._rating = rating

    def get_prep_time(self) -> str:
        return self._prep_time
    
    def set_prep_time(self, prep_time: str) -> None:
        self._prep_time = prep_time

    def get_cook_time(self) -> str:
        return self._cook_time
    
    def set_cook_time(self, cook_time: str) -> None:
        self._cook_time = cook_time

    def get_dietry(self) -> str:
        return self._dietry
    
    def set_dietry(self, dietry: str) -> None:
        self._dietry = dietry
        
    def get_ingredients(self) -> List:
        return self._ingredients 

    def set_ingredients(self, ingredients: List) -> None:
        self._ingredients + ingredients
        
    def get_method(self) -> List:
        return self._method 

    def set_method(self, method: List) -> None:
        self._method + method
    
    def get_recipe(self) -> Dict:
        return {
            "name": self.get_name(),
            "rating": self.get_rating(),
            "prep_time": self.get_prep_time(),
            "cook_time": self.get_cook_time(),
            "ingredients": self.get_ingredients(),
            "method": self.get_method()
        }
    
    def __str__(self):
        return f"A recipe for the dish {self.get_name()}."
