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
                return self.shoppinglists
        elif 'email' in data:
            if self.check_exists(data['email'], 'email'):
                return False
            else:
                self.users.append(data)
                return self.users

    def check_exists(self, check_in, check_for):

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

    def user_logged_in(self):
        """Get a key index for a logged in user"""
        if self.users is not []:
            for user_n in range(0, len(self.users)):
                if self.users[user_n]['email'] == session['user']:
                    return user_n
        return False

    # def store_session(self, data_to_store):
    #     """ Store user/list in session and check there is no other to conflict with"""

    #     if 'email' in data_to_store[0]:
    #         validate = ['email', data_to_store[0]['email']]
    #         if session.get('storage') is None:
    #             session['storage'] = []
    #             session['storage'].append(data_to_store[0])
    #             return "The first user of this session created"
    #         else:
    #             if self.check_in_session('email', validate):
    #                 return "User already exist in session"
    #             else:
    #                 session['storage'].append(data_to_store[0])
    #                 return "User added succesfully in session"

    #     elif 'title' in data_to_store[0]:
    #         validate = ['title', data_to_store[0]['title']]
    #         if self.check_in_session('title', validate):
    #             return False
                
    #         else:
    #             session['storage'][self.user_logged_in()]['shoppinglists'].extend(data_to_store)
    #             return True


    def check_login(self, email, password):
        """Check either data or session login"""
        for log_n in range(0, len(self.users)):
            return bool(email == self.users[log_n]['email'] and check_password_hash(
                        self.users[log_n]['password'], password) is True)


    # def update_data(self, data_to_update):
    #     """Allow user to update his lists"""
    #     if self.check_list(data_to_update['list_id']):
    #         cur_data = self.get_list_data(data_to_update['list_id'])
    #         cur_data['title'] = data_to_update['title']
    #         cur_data['description'] = data_to_update['description']
    #         return self.shoppinglists    

    def get_list_data(self, list_id):
        """ Getting the data for a certain list """

        for list_n in range(0, len(self.shoppinglists)):
            l_data = list_id in self.shoppinglists[list_n].values()
            if l_data is True:
                return self.shoppinglists[list_n]




    # def check_in_session(self, for_check, to_check):
    #     """Check if a user exists in session"""

    #     if for_check == 'email':
    #         if session.get('storage') is not None:
    #             for sess_item in range(0, len(session['storage'])):
    #                 if session['storage'][sess_item][to_check[0]] == to_check[1]:
    #                     return True
    #             return False

    #     elif for_check == 'title':
    #         for l_item in range(0, len(session['storage'][self.user_logged_in()]['shoppinglists'])):
    #             if session['storage'][self.user_logged_in()]['shoppinglists'][l_item][to_check[0]] == to_check[1]:
    #                 return True
    #         return False
    #     else:
    #         return "Invalid search"
    