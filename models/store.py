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
    def email_exists(self, email):
        for sess_n in range(0, len(session['storage'])):
            if (session['storage'][sess_n]['email'] == email):
                 #print(session['storage'][sess_n]['email']+' is '+email)
                return True
            else:
                print(session['storage'][sess_n]['email']+' is '+email)
                return False
    def store_session(self, data_to_store):
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
        session['storage']['shoppinglists'].append(list_to_store)
        	