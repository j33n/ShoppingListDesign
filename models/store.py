""" Our Storage will be stored here """
from flask import session
from werkzeug.security import check_password_hash

class Store(object):
    """ Storage module """
    users = []
    shoppinglists = []
    items = []


    def store_data(self, data):
        """Adding users, lists and items"""

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

    def check_exists(self, check_in, check_for):
        """check if value already exists in storage"""

        if check_for == 'email':
             search = self.users
        elif check_for == 'title':
            search = self.shoppinglists
        elif check_for == 'item_title':
            search = self.items
        else:
            return "Invalid search"
        for sess_n in range(0, len(search)):
                return bool(search[sess_n][check_for] == check_in)

    def user_logged_in_index(self):
        """ Get a key index for a logged in user """

        for user_n in range(0, len(self.users)-1):
            if self.users[user_n]['email'] == session['user']:
                return user_n
        return False

    def get_user_uuid(self):
        if 'user' in session:
            for user_n in range(0, len(self.users)-1):
                if self.users[user_n]['email'] == session['user']:
                     return self.users[user_n]['user_id']
            else:
                return False
        else:
            return "A session 'user' value is missing"


    def check_login(self, email, password):
        """Check if login credentials are valid"""

        for log_n in range(0, len(self.users)):
            if email == self.users[log_n]['email'] and check_password_hash(
                        self.users[log_n]['password'], password) is True:
                return True
        return False

    def shoppinglist_data(self, user_id):
        pass

    def get_list_data(self, list_id):
        """ Getting the data for a certain list """

        for list_n in range(0, len(self.shoppinglists)):
            l_data = list_id in self.shoppinglists[list_n].values()
            if l_data is True:
                return self.shoppinglists[list_n]


    def check_in_session(self, for_check, to_check):
        """Check if a user exists in session"""

        if for_check == 'email':
            for sess_item in range(0, len(self.users)):
                if self.users[sess_item][to_check[0]] == to_check[1]:
                    return True
            return False

        elif for_check == 'title':
            for l_item in range(0, len(self.users[self.user_logged_in_index()]['shoppinglists'])):
                if self.users[self.user_logged_in_index()]['shoppinglists'][l_item][to_check[0]] == to_check[1]:
                    return True
            return False
        else:
            return "Invalid search"