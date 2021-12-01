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

    def check_hashtag(self, hashtag:str):
        check = 0 ## variable to check if item in cart or not a match
        itemList = self.get_items()
        for item in ShoppingCart:
            for item.hashtag in item.hashtags:
                if(item.hashtag == hashtag):
                    return False
        for item in itemList: # iterate through store to check hashtags but not substring
            for item.hashtag in item.hashtags:
                if((item.hashtag == hashtag) and (len(hashtag) == len(item.hashtag))):
                    check = 1
        if check == 1:
            return True
        else:
            return False

    def check_name(self, item_name:str):
        check = 0 ## variable to check if item is in cart or not a match
        itemList = self.get_items()
        for item in ShoppingCart:
            if(item_name == item.name):
                return False
        for item in itemList: ## iterate through the items in the store to see if the search matches
            if((item_name in item.name) or (item_name == item.name)): ## if the search matches/is substring of item
                check = 1            
        if check == 1:
            return True
        else:
            return False


    def search_by_name(self, item_name: str) -> list:
        filtered_list = filter(self.check_name, self.get_items)
        returnList = list(filtered_list)
        sorted_list = returnList.sort(key = lambda x: int(x[1:]))
        sorted_list = sorted_list.sort()
        return sorted_list

    def search_by_hashtag(self, hashtag: str) -> list:
        filtered_list = filter(self.check_hashtag, self.get_items)
        returnList = list(filtered_list)
        sorted_list = returnList.sort(key = lambda x: int(x[1:]))
        sorted_list = sorted_list.sort()
        return sorted_list
        

    def add_item(self, item_name: str):
        count = 0
        itemList = self.get_items()
        for item in self._items:   
            if(item.name == item_name):
                raise ItemAlreadyExistsError("This item already exists")
        for item in itemList:
                if((item_name == item.name) or (item_name in item.name)):
                    if count == 1:
                        raise TooManyMatchesError("Too many items matched")
                    else:
                        ShoppingCart.add_item(self, item)
                        count+=1
        if count == 0:
            raise ItemNotExistError("Item does not Exist Error")
        
            
    def remove_item(self, item_name: str):
        count = 0
        for item in self._items:
            if((item.name == item_name) or (item_name in item.name)):
                count +=1
                if count == 1:
                    ShoppingCart.remove_item(self, item.name)
                elif count > 1:
                    raise TooManyMatchesError("Too many matches found")
        if count == 0:
            raise ItemNotExistError("Item does not exist")

    def checkout(self) -> int:
         return ShoppingCart.get_subtotal(self)