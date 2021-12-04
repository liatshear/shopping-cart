from os import name
import yaml
import collections


from item import Item
from shopping_cart import ShoppingCart
from errors import ItemNotExistError, ItemAlreadyExistsError, TooManyMatchesError


class Store:

    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()
        self.items = []
        
    

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items
    ## get list of hashtags of all items in the store
    def getHashtagList(self) -> list:
        hashtagList = []
        for item in self.items:
            hashtagList.extend(item.hashtags)
        return hashtagList
    ##get list of all the names of the items in the store
    def getNameList(self) -> list:
        nameList = []
        for item in self.items:
            nameList.append(item.name)

    ##helper function to check through hashtag 1) item not in cart 2) item is in store. to be used in the filter method

    def check_hashtag(self, hashtagCheck, item):
        ## iterate through shopping cart to check if item is in cart
        shoppingCarttags = self._shopping_cart.getHashtagList()
        storeTags = self.getHashtagList()
        if hashtagCheck.any(shoppingCarttags): 
             ## item in cart therefore return False
            return False        
        ## if the search matches/is one of the hashtags of thesubstring of item AND not in the cart
        if hashtagCheck.any(storeTags): 
                return True  ## item is in the store AND not in the cart
        ## item is not in cart but also not in store
        return False 

    ## method to check via name 1) item not in cart 2) item exists in store 

    def check_name(item, item_name, self):
        ## iterate through shopping cart to check if item is in cart
        Cartnames = self._shopping_cart.getNameList()
        itemList = self.get_items()
        if item_name.any(Cartnames): 
            return False 
        ## if the search matches/is substring of item in the store
        for item in itemList:
            if item_name in item.name: 
                return True 
        ## item not in cart AND not in store 
        return False 
    
    def sortHashtags(self, returnList):
        countList = []
        HashtagListCart = self._shopping_cart.getHashtagList()
        for item in returnList:
            for item.hashtag in item.hashtags:
                x = HashtagListCart.count(item.hashtag)
                countList.append(x)
        returnList = list(zip(HashtagListCart, countList))
        returnList.sort(key = lambda x: x[1], reverse = True)
        returnListUnzip = list(zip(*returnList))
        returnList = returnListUnzip[0]

    def search_by_name(self, item_name: str) -> list:
        ## filter method to get all items relevant into list, sort by hashtag frequency
        returnList = list(filter(self.check_name(item_name), self.get_items()))  
        returnList.sortHashtags()          
        ##returnList.sort(key=lambda item: (item.name))
        return returnList


    def search_by_hashtag(self, hashtag: str) -> list: ## same as before but now check using hashtag
        hashtagCheck = hashtag
        ## filter method to get all relevant items into a list with hashtag matches
        returnList = list(filter(self.check_hashtag(hashtagCheck), self.get_items()))
        returnList.sortHashtags()
        ##returnList.sort(key=lambda item: item.name)
        return returnList       
        

    def add_item(self, item_name: str):
        count = 0 ## variable to check if there are more then 1 match
        itemList = self.get_items()
        for item in self._shopping_cart.items:   ## begin to iterate through items
            if(item.name == item_name): 
                raise ItemAlreadyExistsError("This item already exists") ## item already in the cart
        for item in itemList: ## look at items in the store
                if((str(item_name) == str(item.name)) or (str(item_name) in str(item.name))): ## find a match in store
                    count +=1 ## each time theres a match
                    itemMatch = item ## save which item it is that matched for the case that there is only one match
        if count > 1: ## more then one match 
            raise TooManyMatchesError("Too many items matched")
        if count == 0: ## no matches
            raise ItemNotExistError("Item does not exist")
        if count == 1: ## exactly one match
            self._shopping_cart.add_item(itemMatch)
             
       
            
    def remove_item(self, item_name: str):
        count = 0 ## variable to check multiple matches
        for item in self._shopping_cart.items:
            if ((item_name == item.name) or (item_name in item.name)):
                count +=1
                itemMatch = item
        if count == 1: ## only one item matched in cart
            self._shopping_cart.remove_item(itemMatch.name)
        if count == 0: ## no items matched 
            raise ItemNotExistError("Item does not exist")
        if count > 1: ## more then one item matched in cart
            raise TooManyMatchesError("Too many matches found")
        

    def checkout(self) -> int:
        if not self._shopping_cart.items:
            return 0
        else:
            return self._shopping_cart.get_subtotal()