""" Our Storage will be stored here """

class Store(object):
    """ Storage module """
    users = []
    shoppinglists = []
    listitems = []

    @staticmethod
    def store_users(arg):
        """Adding users, lists and items"""

        if 'email' in arg:
            Store.users.append(arg)