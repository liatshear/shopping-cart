import yaml
import collections

from item import Item
from shopping_cart import ShoppingCart
from errors import ItemNotExistError, ItemAlreadyExistsError, TooManyMatchesError


class Store:

    items = []
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

    ##helper function to check through hashtag 1) item not in cart 2) item is in store. to be used in the filter method

    def check_hashtag(self, hashtag:str):
        itemList = self.get_items()
        for item in self._shopping_cart.items:
            for item.hashtag in self._shopping_cart.items.hashtags:
                if(item.hashtag == hashtag):
                    return False ## item in cart therefore return False
        for item in self._items: ## iterate through store to check hashtags but not substring
            for item.hashtag in item.hashtags:
                if((item.hashtag == hashtag) and (len(hashtag) == len(item.hashtag))):
                    return True ## item is in the store AND not in the cart
        
        return False ## item is not in cart but also not in store

    ## method to check via name 1) item not in cart 2) item exists in store 

    def check_name(self, item_name:str):
        check = 0 ## variable to check if item is in cart or not a match
        StoreitemList = self.get_items() ## put store items into list
        for item in self._shopping_cart.items: ## iterate through shopping cart to check if item exists
            if(item_name == item.name):
                return False ## item already in cart
        for item in self._items: ## iterate through the items in the store to see if the search matches
            if((item_name in item.name) or (item_name == item.name)): ## if the search matches/is substring of item
                return True ## item not in cart AND in store
        return False ## item not in cart AND not in store 




    def search_by_name(self, item_name: str) -> list:
        returnList = list(filter(self.check_name(item_name), self._items)) ## filter method to get all items relevant into list
        return returnList.sort(key=lambda x: x.get('name'))


    def search_by_hashtag(self, hashtag: str) -> list: ## same as before but now check using hashtag
        returnList = list(filter(self.check_hashtag(hashtag), self._items))
        return returnList.sort(key=lambda x: x.get('name'))
       
        

    def add_item(self, item_name: str):
        count = 0 ## variable to check if there are more then 1 match
        itemList = self.get_items()
        for item in self._shopping_cart.items:   ## begin to iterate through items
            if(item.name == item_name): 
                raise ItemAlreadyExistsError("This item already exists") ## item already in the car
        for item in self._items: ## look at items in the store
                if((item_name == item.name) or (item_name in item.name)): ## find a match in store
                    count +=1 ## each time theres a match
                    itemMatch = item ## save which item it is that matched for the case that there is only one match
        if count > 1: ## more then one match 
            raise TooManyMatchesError("Too many items matched")
        if count == 0: ## no matches
            raise ItemNotExistError("Item does not Exist Error")
        if count == 1: ## exactly one match
            ShoppingCart.add_item(self, itemMatch)
             
       
            
    def remove_item(self, item_name: str):
        count = 0 ## variable to check multiple matches
        for item in self._shopping_cart.items:
            if((item.name == item_name) or (item_name in item.name)):
                count +=1
                itemMatch = item
        if count == 1: ## only one item matched in cart
            ShoppingCart.remove_item(self, itemMatch.name)
        if count == 0: ## no items matched 
            raise ItemNotExistError("Item does not exist")
        if count > 1: ## more then one item matched in cart
            raise TooManyMatchesError("Too many matches found")
        

    def checkout(self) -> int:
        if len(self._shopping_cart.items) == 0:
            return 0
        return ShoppingCart.self._shopping_cart.get_subtotal()