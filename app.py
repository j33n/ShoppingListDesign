# """ module for the routes and views """
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from models.user import User
from models.store import Store
from models.shoppinglist import ShoppingList
from werkzeug.security import generate_password_hash
from datetime import datetime
from forms import RegisterForm, LoginForm, ListForm, EditList

app = Flask(__name__)

# Configurations
import os
app.config.from_object(os.environ['APP_SETTINGS'])
store = Store()
def login_required(f):
	"""Allow some routes to be accessed when logged_in"""

	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Please Log into your ShoppingList Account first')
			return redirect(url_for('login'))
	return wrap

@app.route('/', methods=['GET', 'POST'])
def home():
	error = None
	form = RegisterForm(request.form)
	print(store.users)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(
				username=request.form['username'],
				email=request.form['email'],
				password=generate_password_hash(request.form['password']),
				created_on=datetime.now()
			)	

			# Validates user exists or is saved
			user = new_user.save_user()		
			if user != False:
				session['logged_in'] = True
				session['username'] = request.form['username']
				session['user'] = request.form['email']
				session['index'] = store.user_logged_in_index()
				session['id'] = store.get_user_uuid()
				# print(store.get_user_uuid())
				flash(
					'Welcome ' + session['username']
				)
				print(store.users)
				print(session['index'])
				print(session['id'])
				return redirect(url_for('dashboard'))
			else:
				flash("User already exists")
				return redirect(url_for('home'))
		return render_template("homepage.html", form=form, error=error)
	return render_template("homepage.html", form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	print(store.users)
	if request.method == 'POST':

		if form.validate_on_submit():

			if store.check_login(request.form['username'], request.form['password']):

				session['logged_in'] = True
				session['user'] = request.form['username']
				session['index'] = store.user_logged_in_index()
				session['id'] = store.get_user_uuid()
				# print(store.get_user_uuid())
				flash('Welcome back')
				return redirect(url_for('dashboard'))

			error = 'Invalid Credentials, Try Again'
			return render_template("login.html", form=form, error=error)

		else:
			return render_template("login.html", form=form, error=error)

	return render_template("login.html", form=form, error=error)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	error = None
	form = ListForm(request.form)
	print(store.shoppinglists)
	if request.method == 'POST':
		if form.validate_on_submit():					
			get_id = session['id']
			new_shopping_list = ShoppingList(
				owner_id=get_id,
				title=request.form['title'],
				description=request.form['description'],
				created_on=datetime.now()
			)
			print(session['index'])
			print(session['id'])
			if new_shopping_list.save_list():
				flash('List created successfuly')
				return render_template(
					"dashboard.html",
					form=form,
					data=store.shoppinglists
				)
			flash("List already exists")
			return render_template(
				"dashboard.html",
				form=form,
				data=store.shoppinglists
			)
		return render_template(
			"dashboard.html",
			form=form,
			data=store.shoppinglists,
			error=error
		)
	return render_template(
		"dashboard.html",
		form=form,
		data=store.shoppinglists
	)
@app.route('/edit-list/<list_id>', methods=['GET', 'POST'])
@login_required
def edit_list(list_id):
  """This route allows a user to change a list"""
# Title not updating
  form = EditList(request.form)
  serve_temp = store.get_list_data(list_id)
  if request.method == 'POST':
  	if form.validate_on_submit():
  		renew_list = ShoppingList(
  			owner_id=session['id'],
  			title=request.form['title'],
  			description=request.form['description'],
  			list_id=list_id,
  			created_on=request.form['hidden']
  		)
  		renew_list.update_list()
  		flash('List updated successfuly')
  		return redirect(url_for('dashboard'))
  	
  return render_template(
  	"includes/edit_list.html",
  	form=form,
  	data=store.shoppinglists,
  	form_data=serve_temp
  	)

@app.route('/delete-list/<list_id>')
@login_required
def delete_list(list_id):
	if store.delete_data('shoppinglist', list_id):
		flash("Shopping list deleted succesfully")
		return redirect(url_for('dashboard'))
	flash("Shopping list could not be found")
	return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	session.pop('user', None)
	session.pop('index', None)
	session.pop('id', None)
	session.pop('username', None)
	flash('We hope you enjoyed organizing and sharing lists see you soon')
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)