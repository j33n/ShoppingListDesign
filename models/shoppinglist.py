""" main module for user list """
import uuid
from models.store import Store

class ShoppingList(object):
    """main model class of the a list"""

    def __init__(self, owner_id, title, description, created_on, items=None, list_id=None):
        """ Initialize app """
        self.owner_id = owner_id
        self.list_id = uuid.uuid4().hex if list_id is None else list_id
        self.list_title = title
        self.list_description = description
        self.created_on = created_on
        self.public = False
        self.items = []

    def list_data(self):
        """All list data"""

        return {
            'list_id' : self.list_id,
            'title' : self.list_title,
            'description': self.list_description,
            'owner_id' : self.owner_id,            
            'created_on' : self.created_on,
            'items': self.items
        }


    def save_list(self):
        """Save this list"""

        return Store().store_data(self.list_data())

    def update_list(self):
        """Update a list"""

        return Store().update_data(self.list_data())

        