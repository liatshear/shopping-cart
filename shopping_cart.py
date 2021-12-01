
from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError


class ShoppingCart:
    items = []
    def add_item(self, item: Item):
        if item in self.items:
            raise ItemAlreadyExistsError("Item Already Exists")
        else:
            self.items.append(item)

           
    def remove_item(self, item_name: str):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                break
        else:
            raise ItemNotExistError("Item doesn't Exist Error")

    def get_subtotal(self) -> int:
        total = 0
        for item in self.items:
            total += item.price
        return total
