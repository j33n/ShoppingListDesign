""" Our Storage will be stored here """
from flask import session

class Store(object):
    """ Storage module """

    users = []
    shoppinglists = []
    items = []

    @classmethod
    def store_data(cls, data):
        """Adding users, lists and items"""

        if(data):
        	Store.users.append(data)

    def store_session(self, data_to_store):
    	session['storage'] = data_to_store
    def newlist_session(self, list_to_store):
        session['storage']['shoppinglists'].append(list_to_store)
        	