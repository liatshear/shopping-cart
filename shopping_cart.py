from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError


class ShoppingCart:
    def add_item(self, item: Item):
        if not isinstance(item, Item):
            self.items.append(Item)
        else:
            raise ItemAlreadyExistsError("Item Already Exists Error")


    def remove_item(self, item_name: str):
        if isinstance(str, item):
            self.items.remove(str)
        else:
            raise ItemNotExistError("ItemA NOt Exist Error")

    def get_subtotal(self) -> int:
        total =0
        for self in ShoppingCart:
            total += self.price
        print(total)
