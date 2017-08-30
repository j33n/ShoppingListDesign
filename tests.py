from app import app
import unittest
from flask import Flask
from flask_testing import assert_template_used

class FlaskTestCase(unittest.TestCase):
	"""Testing if all the templates are loading perfectly"""

	render_templates = False

	def setUp(self):
		self.client = app.test_client(self)
		self.user = {
			'username': 'admin',
			'email': 'test@test.com',
			'password': 'secret',
			'confirm_password': 'secret'
		}
		# self.user = [{'created_on': datetime.datetime(2017, 8, 30, 22, 57, 59), 'username': 'admin', 'shoppinglists': [], 'email': 'test@test.com', 'user_id': '53fa07e0da854403baaa8c94af87412e', 'password': 'pbkdf2:sha256:50000$CoCvyXHr$9f73a13d880e02ba2b947d1419803b8e446788d1ee8627e0feb9cf7c7d444a69'}]

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
		"""Ensure pages are loading with a 200 status"""
		response = self.client.get('/login')
		self.assertTrue(b'Enter Your ShoppingList account' in response.data)

	def test_explore(self):
		"""Ensure pages are loading with a 200 status"""
		response = self.client.get('/explore')
		# self.assertTrue(b'Share Your Lists' in response.data)
		self.assert_template_used('mytemplate.html')

	# def test_dashboard(self):
	# 	"""Ensure pages are loading with a 200 status"""
	# 	signup = self.client.post('/', data=self.user)
	# 	# response = self.client.get('/dashboard')
	# 	self.assertTrue(b'Add a new List' in signup.data)

if __name__ == '__main__':
	unittest.main()