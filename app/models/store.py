""" Our Storage will be stored here """
from flask import session
from werkzeug.security import check_password_hash

class Store(object):
    """ Storage module """
    users = []
    shoppinglists = []
    shoppinglistitems = []


    def store_data(self, data):
        """Adding users, shopping lists and items"""

        if "title" in data: 
            if self.check_exists(data['title'], 'title'):
                return False
            self.shoppinglists.append(data)
            return True
        elif 'email' in data:
            if self.check_exists(data['email'], 'email'):
                return False
            self.users.append(data)
            return self.users

        elif 'item_title' in data:
            if self.check_exists(data, 'item_title'):
                return False
            self.shoppinglistitems.append(data)
            return self.shoppinglistitems

    def update_data(self, data_to_update):
        """Allow user to update his shoppinglists"""

        if 'title' in data_to_update:
            shoppinglist_data = self.get_list_data(data_to_update['list_id'])
            shoppinglist_data['title'] = data_to_update['title']
            shoppinglist_data['description'] = data_to_update['description']
            return shoppinglist_data
        shoppinglistitem_data = self.get_item_data(data_to_update['item_id'])
        shoppinglistitem_data['item_title'] = data_to_update['item_title']
        shoppinglistitem_data['item_description'] = data_to_update['item_description']
        return shoppinglistitem_data

    def delete_data(self, type_of_delete, to_delete):
        """Allow a user to delete shopping lists and items"""

        if type_of_delete == "shoppinglist":
            for slist_n in range(len(self.shoppinglists)):
                if self.shoppinglists[slist_n]['list_id'] == to_delete:
                    del self.shoppinglists[slist_n]
                    return True
            return False

        elif type_of_delete == "shoppinglistitem":
            for shoppinglistitem_n in range(len(self.shoppinglistitems)):
                if self.shoppinglistitems[shoppinglistitem_n]['item_id'] == to_delete:
                    del self.shoppinglistitems[shoppinglistitem_n]
                    return True
            return False
        return "We could not find what you are trying to delete"


    def check_exists(self, check_in, check_for):
        """Check if user, shopping list or item already exist in storage"""

        if check_for == 'email':
            search = self.users
        elif check_for == 'title':
            search = self.get_user_lists()
        elif check_for == 'item_title':
            search = self.get_shoppinglists_items(check_in['shoppinglist_id'])
            for sess_n in range(len(search)):
                if search[sess_n][check_for] == check_in['item_title']:
                    return True
            return False
        else:
            return "Invalid search"
        for sess_n in range(len(search)):
            if search[sess_n][check_for] == check_in:
                return True
        return False

    def get_list_data(self, list_id):
        """Getting the data for a certain shopping list"""

        for list_n in range(len(self.shoppinglists)):
            l_data = list_id in self.shoppinglists[list_n].values()
            if l_data is True:
                return self.shoppinglists[list_n]

    def get_item_data(self, item_id):
        """Getting the data for a certain shopping item in a shopping list"""

        for item_n in range(len(self.shoppinglistitems)):
            item_data = item_id in self.shoppinglistitems[item_n].values()
            if item_data is True:
                return self.shoppinglistitems[item_n]
        return False

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
            return False
        return "A session 'user' value is missing"

    def get_user_lists(self):
        """ Get a user logged_in shopping lists """

        shopping_list_to_render = []
        for user_logged in range(len(self.shoppinglists)):
            if self.shoppinglists[user_logged]['owner_id'] == session['id']:
                shopping_list_to_render.append(self.shoppinglists[user_logged])
        return shopping_list_to_render

    def get_shoppinglists_items(self, shoppinglist_id):
        """Get a selected shopping list items"""

        shopping_list_item_to_render = []
        for list_logged in range(len(self.shoppinglistitems)):
            if self.shoppinglistitems[list_logged]['shoppinglist_id'] == shoppinglist_id:
                shopping_list_item_to_render.append(self.shoppinglistitems[list_logged])
        return shopping_list_item_to_render

    def check_login(self, email, password):
        """Check if login credentials are matching with what we have"""

        for log_n in range(len(self.users)):
            if email == self.users[log_n]['email'] and check_password_hash(
                        self.users[log_n]['password'], password) is True:
                return True
        return False
