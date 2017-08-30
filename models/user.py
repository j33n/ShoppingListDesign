""" main module for the user """
import uuid
from models.store import Store

class User(object):
    """main class of the user"""

    def __init__(self, username, email, password, created_on, user_id=None):
        self.username = username
        self.email = email
        self.password = password
        self.user_id = uuid.uuid4().hex if user_id is None else user_id
        self.created_on = created_on

    def user_data(self):
        """All user data"""

        return {
            'user_id' : self.user_id,
            'username' : self.username,
            'email': self.email,
            'password' : self.password,            
            'created_on' : self.created_on
        }

    def store_user(self):
        """Save this user"""
        Store.store_user(self.user_data)

    # def new_user(self, item_name, description, date=datetime.datetime.utcnow()):
    #     """method used for creating a  bucket list"""
    #     item = Item(item_name=item_name,
    #                 description=description,
    #                 owner_id=self._id,
    #                 date=date)
    #     item.save_to_items()

    

    # def save_to_users(self):
    #     """this methods saves data to the users list"""
    #     Data.add_data(self.user_data())