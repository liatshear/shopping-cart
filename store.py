import yaml

from item import Item
from shopping_cart import ShoppingCart
from errors import ItemNotExistError, ItemAlreadyExistsError, TooManyMatchesError


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
        for item in itemList:
            if((item_name in self._items) or (item_name == self._items)):
                ReturnList.append(item)
        sorted_list = ReturnList.sort(key = lambda x: int(x[1:]))
        sorted_list = sorted_list.sort()
        return sorted_list

    def search_by_hashtag(self, hashtag: str) -> list:
        ReturnList = []
        itemList = self.get_items
        for item in itemList:
            if((item.hashtag == hashtag) and (not hashtag in item.hashtag)):
                ReturnList.append(item)
        sorted_list = ReturnList.sort(key = lambda x: int(x[1:]))
        sorted_list = sorted_list.sort()
        return sorted_list

    def add_item(self, item_name: str):
        count = 0
        itemList = self.get_items
        for item in self._shopping_cart:   
            if(item.name == item_name):
                raise ItemAlreadyExistsError("This item already exists")
        for item in itemList:
                if((item_name == item.name) or (item_name in item.name)):
                    if count == 1:
                        raise TooManyMatchesError("Too many items matched")
                    else:
                        self._shopping_cart.append(item)
                        count+=1
        if count == 0:
            raise ItemNotExistError("ItemA NOt Exist Error")
        
            
    def remove_item(self, item_name: str):
        itemList = self.get_items
        count = 0
        for item in itemList:
            if((item.name == item_name) or (item_name in item.name)):
                count +=1
                if count == 1:
                    self._shopping_cart.remove(item)
                elif count > 1:
                    raise TooManyMatchesError("Too many matches found")
        if count == 0:
            raise ItemNotExistError("Item does not exist")

    def checkout(self) -> int:
         return self._shopping_cart.get_subtotal()