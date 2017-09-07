""" main module for user shopping list item """
import uuid
from models.store import Store

class ShoppingListItem(object):
    """main model class of the a shopping list item"""

    def __init__(self, shoppinglist_id, item_title, item_description, created_on, item_id=None):
        """All the item data are passed through our Shopping List Item"""

        self.shoppinglist_id = shoppinglist_id
        self.item_id = uuid.uuid4().hex if item_id is None else item_id
        self.item_title = item_title
        self.item_description = item_description
        self.created_on = created_on

    def item_data(self):
        """All Shopping list item data are returned here"""

        return {
            'item_id' : self.item_id,
            'item_title' : self.item_title,
            'item_description': self.item_description,
            'shoppinglist_id' : self.shoppinglist_id,            
            'created_on' : self.created_on
        }


    def save_sl_item(self):
        """Save this item on it's shopping list"""

        return Store().store_data(self.item_data())

    def update_shoppinglist_item(self):
        """Update an item on the shopping list"""

        return Store().update_data(self.item_data())