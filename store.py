from os import name
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


    def search_by_name(self, item_name: str) -> list:
        returnList = []
        ShoppingCartnames = self._shopping_cart.getNameList()
        HashtagListCart = self._shopping_cart.getHashtagList()
        ##filter method to get all the items that are substrings of store items
        returnListStoreItems = list(filter(lambda item: item_name in item.name, self.get_items()))
        ##only add store items that are also NOT in the shopping cart
        for item in returnListStoreItems:
            if not item_name in ShoppingCartnames:
                returnList.append(item)
        ## count how many times there is a match with a hashtag in the cart item
        countList = []
        for item in returnList:
            count = 0
            ## count the amount of times the hashtags appead in the cart list
            for item.hashtag in item.hashtags:
                count += HashtagListCart.count(item.hashtag)
            countList.append(count)
        ## zip the lists with their item and their count
        returnList = list(zip(returnList, countList))
        ## sort the list based on hashtag frequency
        returnList.sort(key = lambda x: x[1], reverse = True)
        returnListfinal = []
        ## create new list with just the items and not their count
        for r in returnList:
            returnListfinal.append(r[0])              
        returnListfinal.sort(key=lambda item: item.name)
        return returnListfinal


    def search_by_hashtag(self, hashtag: str) -> list: ## same as before but now check using hashtag
        hashtagCheck = hashtag
        returnList = []
        shoppingCarttags = self._shopping_cart.getHashtagList()
        storeTags = self.getHashtagList()
        ## filter method to get all relevant items into a list with hashtag matches
        returnListone = list(filter(lambda item: hashtagCheck in item.hashtags, self.get_items()))
        ##returnList = list(filter(self.check_hashtag, self.get_items()))
        for item in returnListone:
            if not hashtagCheck in shoppingCarttags:
                returnList.append(item)
        countList = []
        HashtagListCart = self._shopping_cart.getHashtagList()
        for item in returnList:
            count = 0
            for item.hashtag in item.hashtags:
                count += HashtagListCart.count(item.hashtag)
            countList.append(count)
        returnList = list(zip(returnList, countList))
        returnList.sort(key = lambda x: x[1], reverse = True)
        returnListfinal = []
        for r in returnList:
            returnListfinal.append(r[0])
        ##returnList.sortHashtags()
        returnListfinal.sort(key=lambda item: item.name)
        return returnListfinal     
        

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