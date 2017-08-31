""" Our Storage will be stored here """
from flask import session

class Store(object):
    """ Storage module """
    def __init__(self):
        self.users = []
        self.shoppinglists = []
        self.items = []


    def store_data(self, data):
        """Adding users, lists and items"""
        if 'title' in data:
            self.shoppinglists.append(data)
            return self.shoppinglists[0]
        elif 'email' in data:
            self.users.append(data)
            return self.users[0]


    def check_list(self, list_to_check):
        """Check if the list is already created"""

        for list_n in range(0, len(self.shoppinglists)):
            return bool(list_to_check in self.shoppinglists[list_n].keys())

    def email_exists(self, email):
        """Check if the user is already registered"""

        for sess_n in range(0, len(session['storage'])):
            if (session['storage'][sess_n]['email'] == email):
                return True
            else:
                return False
        

    def store_session(self, data_to_store):
        """ Store user session and check there is no othe email to conflict"""

        if session.get('storage') is None:
            session['storage'] = []
            session['storage'].append(data_to_store)
            return True
        else:
            if(self.email_exists(data_to_store['email'])):
                return False
            else:
                session['storage'].append(data_to_store)
                return True
            
    def newlist_session(self, list_to_store):
        session['storage'][len(session['storage'])-1]['shoppinglists'].append(list_to_store)
        return True
        	