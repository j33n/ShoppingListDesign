""" main module for the user """
import uuid
from app.models.store import Store

class User(object):
    """main model class of the user"""

    def __init__(self, username, email, password, created_on, user_id=None, shoppinglists=None):
        """ Initialize app """
        self.username = username
        self.email = email
        self.password = password
        self.user_id = uuid.uuid4().hex if user_id is None else user_id
        self.created_on = created_on
        self.shoppinglists = []

    def user_data(self):
        """ All user data """

        return {
            'user_id' : self.user_id,
            'username' : self.username,
            'email': self.email,
            'password' : self.password,            
            'created_on' : self.created_on,
            'shoppinglists' : self.shoppinglists
        }

    def save_user(self):
        """Save this user in a list"""

        return Store().store_data(self.user_data())