""" Our Storage will be stored here """
from flask import session
import datetime

class Store(object):
    """ Storage module """
    def __init__(self):
        self.users = []
        # self.shoppinglists = [
        # {'owner_id': '00ea419d1ce1403eb85a13191e435d18', 'description': 'Lorem', 'items': [], 'title': 'Setting up my first tweeeeeeeeeeeeeeeeeeeeeeeeeeesst', 'list_id': '359fca18acd440028b6e3311860dc89e', 'created_on': datetime.datetime(2017, 9, 1, 12, 13, 10)},
        # {'owner_id': '00ea419d1ce1403eb85a13191e435d18', 'description': 'Lorem', 'items': [], 'title': 'Setting up my first tweet', 'list_id': '29177ccbadf54c4891d7e308921afaef', 'created_on': datetime.datetime(2017, 9, 1, 12, 13, 34)}
        # ]
        self.shoppinglists = []
        self.items = []

    def user_logged_in(self):
        for user_n in range(0, len(session['storage'])):
            if session['storage'][user_n]['email'] == session['user']:
                return user_n


    def store_data(self, data):
        """Adding users, lists and items"""
        if 'title' in data:
            self.shoppinglists.append(data)
            return self.shoppinglists[0]
        elif 'email' in data:
            self.users.append(data)
            return self.users[0]

    def update_data(self, data_to_update):
        """Allow user to update his lists"""
        if self.check_list(data_to_update['list_id']):
            cur_data = self.get_list_data(data_to_update['list_id'])
            cur_data['title'] = data_to_update['title']
            cur_data['description'] = data_to_update['description']
            return self.shoppinglists





    def check_list(self, list_id):
        """" Check list is present """
        
        check_true = []
        for list_n in range(0, len(self.shoppinglists)):            
            check_true.append(list_id in self.shoppinglists[list_n].values())
        if True in check_true:
            return True
        return False

    # def serve_session(self):
    #     self.shoppinglists = session['storage']['shoppinglists']
    #     return self.shoppinglists

    def get_list_data(self, list_id):
        """ Getting the data for a certain list """

        for list_n in range(0, len(self.shoppinglists)):
            l_data = list_id in self.shoppinglists[list_n].values()
            if l_data is True:
                return self.shoppinglists[list_n]

    def email_exists(self, email):
        """Check if the user is already registered"""

        for sess_n in range(0, len(session['storage'])):
            if session['storage'][sess_n]['email'] == email:
                return True
            else:
                return False
        

    def store_session(self, data_to_store):
        """ Store user session and check there is no other email to conflict"""

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
        	