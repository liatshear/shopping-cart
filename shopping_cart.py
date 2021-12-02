import itertools
from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError


class ShoppingCart:
    items = []

    def add_item(self, item: Item):
        if item not in self.items: ## check if item isnt already in cart
            self.items.append(item) ## add item to cart
        else: ## item is already in cart
            raise ItemAlreadyExistsError("Item Already Exists")
            
           
    def remove_item(self, item_name: str):
        for item in self.items:
            if item.name == item_name or item_name in item.name:
                self.items.remove(item) ## remove from cart  
                break            
                     ## item not in cart
        raise ItemNotExistError("Item does not exist")

    def get_subtotal(self) -> int:
        if not self.items:
            return 0
        return sum(item.price for item in self.items) - 10

