from _typeshed import Self
from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError


class ShoppingCart:
    def add_item(self, item: Item):
        if item not in self.items:
            self._items.append(item)
        else:
            raise ItemAlreadyExistsError("Item Already Exists")


    def remove_item(self, item_name: str):
        for item in self.items:
            if item.name == item_name:
                self._items.remove(item)
                break
        else:
            raise ItemNotExistError("Item doesn't Exist Error")

    def get_subtotal(self) -> int:
        total = 0
        for item in self._items:
            total += item.price
        return total
