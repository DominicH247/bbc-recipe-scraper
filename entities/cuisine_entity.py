from typing import List, Dict

class Cuisine:
    def __init__(self, name: str="",  availeable_count: int=0, recipes: List=[]):
        self._name = name
        self._available_count = int(availeable_count)
        self._recipes = recipes
        self._recipe_count = int(len(self._recipes))

    def get_name(self) -> str:
        return self._name
    
    def set_name(self, name: str) -> None:
        self._name = name
    
    def get_recipe_count(self) -> str:
        return self._recipe_count

    def set_recipe_count(self) -> None:
        self._recipe_count = int(len(self._recipes))
    
    def get_recipes(self) -> List:
        return self._recipes

    def set_recipes(self, recipes: List) -> None:
        self._recipes + recipes
        self.set_recipe_count()
    
    def get_available_count(self) -> List:
        return self._available_count

    def set_available_count(self, available_count: int) -> None:
        self._available_count = available_count
    
    def get_cuisine(self) -> Dict:
        return {
            "name": self.get_name(),
            "recipe_count": self.get_recipe_count(),
            "available_count": self.get_available_count(),
            "recipes": self.get_recipes()
        }
    
    def __str__(self):
        return f"A {self.get_name()} cuisine, which has {self.get_recipes_count()} available recipes."
    