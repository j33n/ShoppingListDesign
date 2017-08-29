from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
	"""Testing if all the templates are loading perfectly"""

	def setUp(self):
		self.client = app.test_client(self)

	def test_all_page_loads(self):
		"""Ensure pages are loading with a 200 status"""
		pages = ['/', '/login', '/explore', '/dashboard']
		for page in pages:
			response = self.client.get(page, content_type='html/text')
			self.assertEqual(response.status_code, 200)

	def test_homepage(self):
		response = self.client.get('/')
		self.assertTrue(b'Keep track of your shopping' in response.data)

	def test_login(self):
		response = self.client.get('/login')
		self.assertTrue(b'Enter Your ShoppingList account' in response.data)

	def test_explore(self):
		response = self.client.get('/explore')
		self.assertTrue(b'Share Your Lists' in response.data)

	def test_dashboard(self):
		response = self.client.get('/dashboard')
		self.assertTrue(b'Add a new List' in response.data)

if __name__ == '__main__':
	unittest.main()