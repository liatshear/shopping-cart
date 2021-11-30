
from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError


class ShoppingCart:
    def add_item(self, item: Item):
        if item in self._shopping_cart:
            raise ItemAlreadyExistsError("Item Already Exists")
        else:
            self._shopping_cart.append(item)

           
    def remove_item(self, item_name: str):
        for item in self._shopping_cart:
            if item.name == item_name:
                self._shopping_cart.remove(item)
                break
        else:
            raise ItemNotExistError("Item doesn't Exist Error")

    def get_subtotal(self) -> int:
        total = 0
        for item in self._shopping_cart:
            total += item.price
        return total
