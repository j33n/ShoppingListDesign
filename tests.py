from app import app
import unittest

class FlaskTestCase(unittest.TestCase):


	def setUp(self):
		self.client = app.test_client(self)
		self.user = {
			'username': 'admin',
			'email': 'test@test.com',
			'password': 'secret',
			'confirmpassword': 'secret'
		}
		
	def test_all_page_loads(self):
		"""Ensure pages are loading with a 200 status"""
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
	def test_user_signup(self):
		"""Test user signup"""
		response = self.client.post(
			'/',
			data=self.user,
			follow_redirects=True
		)
		self.assertTrue(b'Add a new List' in response.data)

	def test_user_logout(self):
		self.client.post(
			'/',
			data=self.user,
			follow_redirects=True
		)
		response = self.client.get(
			'/logout',
			follow_redirects=True
		)
		self.assertTrue(b'We hope you enjoyed organizing and sharing lists see you soon' in response.data)

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
			data=dict(username='test@test.com', password="secret"),
			follow_redirects=True
		)
		self.assertTrue(b'Welcome back' in response.data)

	def test_account_duplication(self):
		account1 = self.client.post(
			'/',
			data=self.user,
			follow_redirects=True
		)
		account2 = self.client.post(
			'/',
			data=self.user,
			follow_redirects=True
		)
		account3 = self.client.post(
			'/',
			data=self.user,
			follow_redirects=True
		)
		self.assertTrue(b'Add a new List' in account1.data)
		self.assertTrue(b'User already exists' in account2.data)
		self.assertTrue(b'User already exists' in account3.data)



if __name__ == '__main__':
	unittest.main()