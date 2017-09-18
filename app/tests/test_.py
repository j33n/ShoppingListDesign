import unittest
from flask import url_for
from app.models.store import Store
from app import app, create_app


class FlaskClientTestCase(unittest.TestCase):
    """This class will test how data is manipulated in Store"""

    def setUp(self):
        """Prepare the data to use through tests"""
        
        self.client = app.test_client(use_cookies=True)

        self.shoppinglist = Store.shoppinglists
        self.user = Store.users
        self.items = Store.shoppinglistitems
        self.myuser = {
            'username': 'admin',
            'email': 'testaiueo@test.com',
            'password': 'secret',
            'confirmpassword': 'secret'
        }
        self.myshoppinglist = {
            'list_id': '3b59d76bf7e5431c96d5feb156c5d468',
            'title': 'To cook',
            'description': 'Items to make my favorite meal',
            'owner_id': '68ac9d4fd392457e911abc8c3f68e6ed',
            'created_on': 'date'
        }
        self.myitem = {
            'item_id': 'a898000d6d644eecbdd38c87e781a186',
            'item_title': 'Vitunguu',
            'item_description': 'Vitunguu for nyama',
            'shoppinglist_id': '3b59d76bf7e5431c96d5feb156c5d468',
            'created_on': 'date'
        }

    def tearDown(self):
        """Clear all data set up"""

        self.shoppinglist = None
        self.user = None
        self.items = None

    def test_all_storage(self):
        """Test we have our storage ready"""

        self.assertIsInstance(self.shoppinglist, list)
        self.assertIsInstance(self.user, list)
        self.assertIsInstance(self.items, list)

    def test_data_can_be_stored(self):
        """Test a User can be stored"""

        store = Store()
        user2 = {
            'username': 'MrsAdmin',
            'email': 'Mrsadmin@test.com',
            'password': 'secret',
            'confirmpassword': 'secret'
        }
        store_data = store.store_data(self.myuser)
        self.assertTrue(store_data)
        size_before = len(store.users)
        store_duplicate = store.store_data(self.myuser)
        self.assertFalse(store_duplicate)
        store.store_data(user2)
        size_after = len(store.users)
        self.assertEqual(size_after-size_before, 1)

    def test_can_store_item_and_list(self):
        """Test if shopping lists and items can be stored"""

        store = Store()
        with self.client:
            self.client.post('/', data=dict(
                username="Fonsi",
                email="fonsi@test.com",
                password="secret",
                confirmpassword="secret"
            ),
                follow_redirects=True)
            store_shoppiglist = store.store_data(self.myshoppinglist)
            store_shoppiglistitem = store.store_data(self.myitem)
            self.assertTrue(store_shoppiglist)
            self.assertEqual(store_shoppiglistitem[0][
                             'item_id'], self.myitem['item_id'])

    def test_update_shoppinglist_item(self):
        """Test if user can update shoppinglist and item"""

        store = Store()
        with self.client:
            self.client.post('/login', data=dict(
                username="fonsi@test.com",
                password="secret",
            ),
                follow_redirects=True)

            store.store_data(self.myshoppinglist)
            for_update = {
                'list_id': '3b59d76bf7e5431c96d5feb156c5d468',
                'title': 'To wear',
                'description': 'Items to make my favorite clothes',
            }
            update_shoppinglist = store.update_data(for_update)
            self.assertTrue(update_shoppinglist)

    def test_delete_shoppinglist(self):
        """Test if user can delete shoppinglist and item"""

        store = Store()
        with self.client:
            self.client.post('/login', data=dict(
                username="fonsi@test.com",
                password="secret",
            ),
                follow_redirects=True)
        before_deletion = len(store.shoppinglists)
        delete_list = store.delete_data(
            'shoppinglist', '3b59d76bf7e5431c96d5feb156c5d468')
        after_deletion = len(store.shoppinglists)
        self.assertTrue(delete_list)
        self.assertEqual(before_deletion - after_deletion, 1)


if __name__ == '__main__':
    unittest.main()
