from datetime import datetime
import unittest
from app import app

from app.models.store import Store
from app.models.shoppinglist import ShoppingList
from app.models.shoppinglistitem import ShoppingListItem

class FlaskTestCase(unittest.TestCase):
	"""All Tests"""

	def setUp(self):
		self.client = app.test_client(self)
		self.user = {
			'username': 'admin',
			'email': 'testaiueo@test.com',
			'password': 'secret',
			'confirmpassword': 'secret'
		}

	def tearDown(self):
		self.user = None
		self.client = None

	def accounts(self, username, email, password, confirmpassword):
		"""Setup a testing registration"""

		return self.client.post(
			'/',
			data={
				'username':username,
				'email':email,
				'password':password,
				'confirmpassword':confirmpassword
			},
			follow_redirects=True
		)

	def login(self, email, password):
		"""Setup a testing login"""

		return self.client.post(
			'/login',
			data={
				'username':email,
				'password':password
			},
			follow_redirects=True
		)

	def shoppinglists(self, title, description):
		"""Setup a testing shopping list"""

		my_shoppinglist = dict(
			title=title,
			description=description
		)		
		response = self.client.post(
			'/dashboard',
			data=my_shoppinglist,
			follow_redirects=True
		)
		return response

	def test_all_page_loads(self):
		"""Ensure pages are loading with a 200 status"""

		pages = ['/', '/login']
		for page in pages:
			response = self.client.get(page, content_type='html/text')
			self.assertEqual(response.status_code, 200)

	def test_homepage(self):
		""" Test homepage renders template """

		response = self.client.get('/')
		self.assertTrue(b'Keep track of your shopping' in response.data)

	def test_login(self):
		"""Test login page is rendering"""

		response = self.client.get('/login')
		self.assertTrue(b'Enter Your ShoppingList account' in response.data)

	def test_user_signup(self):
		"""Test user signup"""

		response = self.accounts('Pacito', 'pacito@test.com', 'secret', 'secret')
		self.assertTrue(b'Welcome Pacito' in response.data)

	def test_incorrect_login(self):
		"""Ensure incorrect data can't login"""

		self.accounts('burito', 'burito@test.com', 'secret', 'secret')
		self.client.get(
			'/logout',
			follow_redirects=True
		)
		response = self.login('Incorrect@test.com', 'Incorrect')
		self.assertTrue(b'Invalid Credentials, Try Again' in response.data)

	def test_wrong_data(self):
		"""Test if our signup form is valid"""
		
		response1 = self.accounts('uwouwo', 'uwouwo.test.com', 'secret', 'secret')
		self.assertIn(b'Invalid email address', response1.data)
		response2 = self.accounts('Puerto', 'uwouwo@test.com', 'pokito', 'pokito1')
		self.assertIn(b'Passwords must match', response2.data)
		response3 = self.accounts('Rico', 'uwouwo@test.com', 'pacito', 'pacito')
		self.assertIn(b'Field must be between 5 and 50 characters', response3.data)

	def test_two_account_inservice(self):
		"""Ensure two account can't be active at once"""

		response1 = self.accounts('Favorito', 'favorito@test.com', 'secret', 'secret')
		response2 = self.accounts('Favorito', 'favorito@test.com', 'secret', 'secret')
		self.assertIn(b'Welcome Favorito', response1.data)
		self.assertIn(b'Another account already in service', response2.data)

	def test_user_login(self):
		"""Ensure user can login"""
		self.accounts = ('burito', 'burito@test.com', 'secret', 'secret')
		self.client.get(
			'/logout',
			follow_redirects=True
		)
		response = self.login('burito@test.com', 'secret')
		self.assertTrue(b'Welcome back' in response.data)

	def test_user_add_shoppinglist(self):
		"""Ensure user can add a shopping list"""

		self.login('burito@test.com', 'secret')
		response = self.shoppinglists('My test shopping list', 'Buy sandals')
		self.assertIn(b"List created successfuly", response.data)


	def test_new_shoppinglist(self):
		"""User new shopping list data are available"""

		shoppinglist = ShoppingList(
			'0451cfdc39ef47bcb4b595617d7fa4cd',
			'Tech stuff',
			'RasberryPi',
			datetime.now()
		)
		shoppinglist.list_data()
		self.assertIsInstance(shoppinglist.list_data(), dict)
		self.assertEqual(shoppinglist.list_data()['title'], 'Tech stuff')


	def test_check_login(self):
		self.accounts = ('burito', 'burito@test.com', 'secret', 'secret')
		login_check = Store().check_login('burito@test.com', 'secret')
		self.assertTrue(login_check)

	def test_user_logout(self):
		"""Test user can logout"""

		self.accounts('Despacito', 'despacito@test.com', 'secret', 'secret')
		response = self.client.get(
			'/logout',
			follow_redirects=True
		)
		self.assertTrue(b'We hope you enjoyed organizing and sharing lists see you soon' in response.data)

if __name__ == '__main__':
	unittest.main()