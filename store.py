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

    ## get list of hashtags of all items in the store same as shopping cart
    def getHashtagList(self) -> list:
        hashtagList = []
        for item in self.items:
            hashtagList.extend(item.hashtags)
        return hashtagList


    def search_by_name(self, item_name: str) -> list:
        itemMatches = []
        ShoppingCartnames = self._shopping_cart.getNameList()
        HashtagListCart = self._shopping_cart.getHashtagList()
        ##filter method to get all the items that are substrings of store items into a list
        StoreItemMatches = list(filter(lambda item: item_name in item.name, self.get_items()))
        ##only add store items that are also NOT in the shopping cart
        for item in StoreItemMatches:
            if item.name not in ShoppingCartnames:
                itemMatches.append(item)
        ## count how many times there is a match with a hashtag in the cart item
        countList = []
        for item in itemMatches:
            count = 0
            ## count the amount of times the hashtags appear in the cart hashtags list
            for item.hashtag in item.hashtags:
                count += HashtagListCart.count(item.hashtag)
            countList.append(count)
        ## zip the lists with their item and their count of matches of hashtags and sorts based on hashtag freq
        itemMatches = list(zip(itemMatches, countList))
        itemMatches.sort(key = lambda x: x[1], reverse = True)
        returnList = []
        ## create new list with just the items and not their count
        for r in itemMatches:
            returnList.append(r[0])   
        ## now sort lexicographically the names           
        returnList.sort(key=lambda item: item.name)
        return returnList


    def search_by_hashtag(self, hashtag: str) -> list: ## same as before but now check using hashtag
        itemMatches = []
        shoppingCartNames = self._shopping_cart.getNameList()
        HashtagListCart = self._shopping_cart.getHashtagList()
        ## filter method to get all relevant items into a list with hashtag matches in the store
        StoreMatches = list(filter(lambda item: hashtag in item.hashtags, self.get_items()))
        ## now only add items from the list that are NOT in the shopping cart
        for item in StoreMatches:
            if item.name not in shoppingCartNames:
                itemMatches.append(item)
        ## create a count list to see the frequency of hashtags in the shopping cart
        countList = []
        for item in itemMatches:
            count = 0
            for item.hashtag in item.hashtags:
                count += HashtagListCart.count(item.hashtag)
            countList.append(count)
        itemMatches = list(zip(itemMatches, countList))
        itemMatches.sort(key = lambda x: x[1], reverse = True)
        ## create final return list with just the items
        returnList = []
        for r in itemMatches:
            returnList.append(r[0])
        ## sort the items in lexicographic order
        returnList.sort(key=lambda item: item.name)
        return returnList     
        

    def add_item(self, item_name: str):
        count = 0 
        itemList = self.get_items()
        ## iterate through cart to check if item exists
        for item in self._shopping_cart.items: 
            ## in the case the item is already in the cart
            if(item.name == item_name): 
                raise ItemAlreadyExistsError("This item already exists")
            ## checks the item is in the store as a substring or the actual item 
        for item in itemList: 
            if((item_name == item.name) or (item_name in item.name)): 
                ## each time we find a match add one and keep track of which item was a match
                count +=1 
                itemMatch = item 
        ## check if there were multiple, no matches or only one and then add it to the cart if all conditions met
        if count > 1: 
            raise TooManyMatchesError("Too many items matched")
        if count == 0: 
            raise ItemNotExistError("Item does not exist")
        if count == 1:
            self._shopping_cart.add_item(itemMatch)
             
       
            
    def remove_item(self, item_name: str):
        count = 0 
        ## iterate through cart to see if there is a match substring or the item in the cart
        for item in self._shopping_cart.items:
            if ((item_name == item.name) or (item_name in item.name)):
                ## count how many matches and keep track of which item matched
                count +=1
                itemMatch = item
        ## check if one match and remove from cart, or no matches/too many matches
        if count == 1:
            self._shopping_cart.remove_item(itemMatch.name)
        if count == 0:  
            raise ItemNotExistError("Item does not exist")
        if count > 1: 
            raise TooManyMatchesError("Too many matches found")
        

    def checkout(self) -> int:
        ## check the cart isnt empty
        if self._shopping_cart.items:
            return self._shopping_cart.get_subtotal()
        ## the list is empty
        else:
            return 0