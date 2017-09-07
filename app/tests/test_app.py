import unittest
from app import app
from app.models.store import Store

class FlaskTestCase(unittest.TestCase):

	def setUp(self):
		self.client = app.test_client(self)
		self.user = {
			'username': 'fortestusernme',
			'email': 'fortestname@fortestname.com',
			'password': 'password',
			'confirmpassword': 'password'
		}

	def tearDown(self):
	  self.client = None
	  self.user = None
	  Store().users = []
	  Store().shoppinglists = []
	  Store().shoppinglistitems = []

	def test_all_page_loads(self):
		"""Ensure homepage, login and explore are loading with a 200 status"""

		pages = ['/', '/login', '/explore']
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

	def test_explore(self):
		"""Test explore page is rendering"""

		response = self.client.get('/explore')
		self.assertTrue(b'Share Your Lists' in response.data)

	def test_incorrect_login(self):
		self.client.post(
			'/',
			data=self.user,
			follow_redirects=True
		)
		self.client.get(
			'/logout',
			follow_redirects=True
		)
		response = self.client.post(
			'/login',
			data=dict(username='Incorrect@test.com', password="Incorrect"),
			follow_redirects=True
		)
		self.assertTrue(b'Invalid Credentials, Try Again' in response.data)

	def test_user_login(self):
		self.client.post(
			'/',
			data=self.user,
			follow_redirects=True
		)
		self.client.get(
			'/logout',
			follow_redirects=True
		)
		response = self.client.post(
			'/login',
			data=dict(
				username='fortestemail@fortestemail.com',
				password="password"
			),
			follow_redirects=True
		)
		return response
		self.assertTrue(b'Welcome back' in response.data)


if __name__ == '__main__':
	unittest.main()