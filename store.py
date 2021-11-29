import yaml

from item import Item
from shopping_cart import ShoppingCart

class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def search_by_name(self, item_name: str) -> list:
           ReturnList = []
        itemList = self.get_items
        for items in itemList:
            if(str in Item) or (isinstance(str, Item)):
                ReturnList.append(Item)
        return ReturnList.sort()

    def search_by_hashtag(self, hashtag: str) -> list:
          ReturnList = []
        itemList = self.get_items
        for items in itemList:
            if (Item.hashtag == str) and (not isinstance(str, Item.hashtag)):
                ReturnList.append(Item)
        return ReturnList.sort()

    def add_item(self, item_name: str):
        count = 0
        itemList = self.get_items
        if isinstance(str, self._shopping_cart):
            raise ItemAlreadyExistsError("This item already Exists")
        for items in itemList:
            if (str == Item.name) or (str in Item.name):
                self.shopping_cart.add_item(self, Item)
                count+= 1
        if count == 0:
            raise ItemNotExistError("ItemA NOt Exist Error")
        if count > 1:
            raise TooManyMatchesError("Too many items matched")

    def remove_item(self, item_name: str):
        itemList = self.get_items
        count = 0
        for items in itemList:
            if (Item.name == str) or (str in Item.name):
                count +=1
                if count == 1:
                    self._shopping_cart.remove_item(self, str)
                else:
                    raise TooManyMatchesError("Too many matches found")
        if count == 0:
            raise ItemNotExistError("Item does not exist")

    def checkout(self) -> int:
         return self._shopping_cart.get_subtotal(self)
