from datetime import datetime
import unittest
from app import app

from app.models.store import Store
from app.models.shoppinglist import ShoppingList
from app.models.shoppinglistitem import ShoppingListItem

class StoreTestCase(unittest.TestCase):
	"""All Tests"""

	def setUp(self):
		self.client = app.test_client(self)
		self.user = {
			'user_id' : '68ac9d4fd392457e911abc8c3f68e6ed',
            'username' : 'John',
            'email': 'johndoe@test.com',
            'password' : 'secret',            
            'created_on' : 'date',
            'shoppinglists' : []
		}
		self.shoppinglist = {
			'list_id' : '3b59d76bf7e5431c96d5feb156c5d468',
            'title' : 'To cook',
            'description': 'Items to make my favorite meal',
            'owner_id' : '68ac9d4fd392457e911abc8c3f68e6ed',            
            'created_on' : 'date',
            'items': []
		}
		self.shoppinglistitems = {
            'item_id' : 'a898000d6d644eecbdd38c87e781a186',
            'item_title' : 'Vitunguu',
            'item_description': 'Vitunguu for nyama',
            'shoppinglist_id' : '3b59d76bf7e5431c96d5feb156c5d468',            
            'created_on' : 'date'
		}

	def tearDown(self):
		self.user = None
		self.client = None
		self.shoppinglistitems = None
		self.shoppinglist = None
		self.user = None
		
	def test_store_data(self):
		"""check if a user can be stored"""
		
		storage_before = len(Store().users)
		store = Store().store_data(self.user)
		storage_after = len(Store().users)
		self.assertEqual(storage_after - storage_before, 1)
		self.assertIsInstance(store, list)


if __name__ == '__main__':
	unittest.main()