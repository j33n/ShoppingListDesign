""" Our Storage will be stored here """
from flask import session
from werkzeug.security import check_password_hash

class Store(object):
    """ Storage module """
    users = []
    shoppinglists = []
    items = []


    def store_data(self, data):
        """Adding users, shopping lists and items"""

        if 'title' in data: 
            if self.check_exists(data['title'], 'title'):
                return False
            else:
                self.shoppinglists.append(data)
                return True
        elif 'email' in data:
            if self.check_exists(data['email'], 'email'):
                return False
            else:
                self.users.append(data)
                return self.users

    def update_data(self, data_to_update):
        """Allow user to update his shoppinglists"""

        if 'title' in data_to_update:
            if self.check_exists(data_to_update['title'], 'title'):
                cur_data = self.get_list_data(data_to_update['list_id'])
                cur_data['title'] = data_to_update['title']
                cur_data['description'] = data_to_update['description']
                return data_to_update['title']

    def delete_data(self, type_of_delete, to_delete):
        """Allow a user to delete shopping lists and items"""

        if type_of_delete == "shoppinglist":
            for slist_n in range(len(self.shoppinglists)):
                if self.shoppinglists[slist_n]['list_id'] == to_delete:
                    del self.shoppinglists[slist_n]
                    return True
            return False

        elif type_of_delete == "shoppingitem":
            return "Fucked"

        else:
            return "We could not find what you are trying to delete"


    def check_exists(self, check_in, check_for):
        """Check if value already exists in storage"""

        if check_for == 'email':
             search = self.users
        elif check_for == 'title':
            search = self.shoppinglists
        elif check_for == 'item_title':
            search = self.items
        else:
            return "Invalid search"
        for sess_n in range(len(search)):
                return bool(search[sess_n][check_for] == check_in)

    def get_list_data(self, list_id):
        """Getting the data for a certain shopping list"""

        for list_n in range(len(self.shoppinglists)):
            l_data = list_id in self.shoppinglists[list_n].values()
            if l_data is True:
                return self.shoppinglists[list_n]

    def user_logged_in_index(self):
        """Get a key index for a logged in user"""

        for user_n in range(len(self.users)):
            if self.users[user_n]['email'] == session['user']:
                return user_n
        return False

    def get_user_uuid(self):
        """ Get a user uuid to be used as a foreign key """

        if 'user' in session:
            for user_n in range(len(self.users)):
                if self.users[user_n]['email'] == session['user']:
                     return self.users[user_n]['user_id']
            else:
                return False
        else:
            return "A session 'user' value is missing"


    def check_login(self, email, password):
        """Check if login credentials are matching with what we have"""

        for log_n in range(len(self.users)):
            if email == self.users[log_n]['email'] and check_password_hash(
                        self.users[log_n]['password'], password) is True:
                return True
        return False