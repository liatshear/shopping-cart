from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError


class ShoppingCart:

    def __init__(self):
        self.items = []

    def add_item(self, item: Item):
        if item not in self.items: ## check if item isnt already in cart
            self.items.append(item) ## add item to cart
        else: ## item is already in cart
            raise ItemAlreadyExistsError("Item Already Exists")
            
           
    def remove_item(self, item_name: str):
        for item in self.items:
            if (str(item.name) == str(item_name)):
                self.items.remove(item) ## remove from cart  
                return               
        ## item not in cart
        raise ItemNotExistError("Item does not exist")

    def get_subtotal(self) -> int:
        if self.items:
            ## iterate through to get the price and add to the total price
            return sum(item.price for item in self.items)
            ## the list is empty
        else:
            return 0

    def getHashtagList(self) -> list:
        hashtagList = []
        ## iterate through items and add their individual hashtags to a list
        for item in self.items:
            hashtagList.extend(item.hashtags)
        return hashtagList

    def getNameList(self) -> list:
        nameList = []
        ## iterate through and get the names of all the items in the shopping cart
        for item in self.items:
            nameList.append(item.name)
        return nameList