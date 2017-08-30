""" Our Storage will be stored here """

class Store(object):
    """ Storage module """

    users = [{'username':'John'}]
    shoppinglists = []
    listitems = []

    @classmethod
    def store_users(cls, user_data):
        """Adding users, lists and items"""

        if(user_data):
        	Store.users.append(user_data)
        	