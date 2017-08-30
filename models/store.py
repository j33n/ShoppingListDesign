""" Our Storage will be stored here """
from flask import session

class Store(object):
    """ Storage module """

    users = []
    shoppinglists = []
    items = []

    @classmethod
    def store_users(cls, user_data):
        """Adding users, lists and items"""

        if(user_data):
        	Store.users.append(user_data)

    def store_session(self, data_to_store):
    	session['storage'] = data_to_store
        	