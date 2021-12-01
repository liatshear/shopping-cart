
from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError


class ShoppingCart:
    items = [] ## initialize items in shopping cart
    def add_item(self, item: Item):
        if item not in self.items: ## check if item isnt already in cart
            self.items.append(item) ## add item to cart
        else: ## item is already in cart
            raise ItemAlreadyExistsError("Item Already Exists")
            

           
    def remove_item(self, item_name: str):
        for item in self.items:
            if item.name == item_name: ## check if the item name is in cart
                self.items.remove(item) ## remove from cart
                break
        else: ## item not in cart
            raise ItemNotExistError("Item doesn't Exist Error")

    def get_subtotal(self) -> int:
        total = 0
        if not self.items:
            return 0
        for item in self.items: ## iterate through items
            total += item.price ## each time add the price of the item
        return total
