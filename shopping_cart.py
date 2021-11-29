from item import Item


class ShoppingCart:
    def add_item(self, item: Item):
        if not isinstance(Item, self): 
            self.items.append(Item)
        else:
            raise ItemAlreadyExistsError("Item Already Exists Error")          


    def remove_item(self, item_name: str):
        # TODO: Complete
        pass

    def get_subtotal(self) -> int:
        # TODO: Complete
        pass
