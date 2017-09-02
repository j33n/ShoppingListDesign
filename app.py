# """ module for the routes and views """
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from models.user import User
from models.store import Store
from models.shoppinglist import ShoppingList
from werkzeug.security import generate_password_hash, \
     check_password_hash
from datetime import datetime
from forms import RegisterForm, LoginForm, ListForm, EditList

app = Flask(__name__)

# Configurations
import os
app.config.from_object(os.environ['APP_SETTINGS'])

def login_required(f):
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
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(
				username=request.form['username'],
				email=request.form['email'],
				password=generate_password_hash(request.form['password']),
				created_on=datetime.now()
			)			
			new_user.save_user()			
			if(Store().store_session(new_user.user_data())):
				flash(
					'Welcome ' + session['storage']
					[len(session['storage'])-1]
					['username']
				)
				session['logged_in'] = True				
				return redirect(url_for('dashboard'))
			else:
				flash("User already exists")
				error = "User already exists"
				return redirect(url_for('home'))
		return render_template("homepage.html", form=form, error=error)
	return render_template("homepage.html", form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			if(request.form['username'] != session['storage'][len(session['storage'])-1]['email'])\
				or check_password_hash(
					session['storage'][len(session['storage'])-1]['password'], request.form['password']) is False:
				error = 'Invalid Credentials, Try Again'
			else:
				session['logged_in'] = True
				flash('Welcome back ' + session['storage'][len(session['storage'])-1]['username'])
				return redirect(url_for('dashboard'))
		else:
			return render_template("login.html", form=form, error=error)
	return render_template("login.html", form=form, error=error)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = ListForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_list = ShoppingList(
				owner_id=session['storage'][len(session['storage'])-1]['user_id'],
				title=request.form['title'],
				description=request.form['description'],
				created_on=datetime.now()
			)
			new_list.save_list()
			add_to_session(new_list.save_list())
			flash('List created successfuly')
			return render_template(
				"dashboard.html",
				form=form,
				data=serve_list()
			)
		return render_template(
			"dashboard.html",
			form=form,
			data=serve_list()
		)
	return render_template(
		"dashboard.html",
		form=form,
		data=serve_list()
	)

def add_to_session(session_value):
	session['storage'][len(session['storage'])-1]['shoppinglists'].append(session_value)
	return session['storage']

def serve_list():
	if session.get('storage') is not None:
		all_lists = session['storage'][len(session['storage'])-1]['shoppinglists']
		return all_lists

@app.route('/edit-list/<list_id>')
@login_required
def edit_list(list_id, methods=['GET', 'POST']):
	"""This route allows a user to change a list"""
	# print(serve_list())
	form = EditList(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			renew_list = ShoppingList(
				owner_id=session['storage'][len(session['storage'])-1]['user_id'],
				title=request.form['title'],
				description=request.form['description'],
				list_id=list_id,
				created_on=request.form['hidden']
			)
			renew_list.update_list(list_id)
	
	store = Store()
	if store.check_list(list_id):
		flash('You can edit your list here')
		serve_temp = store.get_list_data(list_id)
		return render_template(
			"includes/edit_list.html",
			form=form,
			data=serve_list(),
			form_data=serve_temp
		)
	flash('list can not be found')


# @app.route('/add-item/<list_id>')
# def add_item(list_id):
# 	form = ListForm(request.form)
# 	Store().edit_lists(list_id)
# 	flash('This functionality is still in maintenance')
# 	return render_template(
# 		"dashboard.html",
# 		form=form,
# 		data=serve_list()
# 	)


# @app.route('/delete-list/<list_id>')
# def delete_list(list_id):
# 	form = ListForm(request.form)
# 	Store().edit_lists(list_id)
# 	flash('This functionality is still in maintenance')
# 	return render_template(
# 		"dashboard.html",
# 		form=form,
# 		data=serve_list()
# 	)

@app.route('/explore')
def explore():
	return render_template("explore.html")

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	session.pop('email', None)
	flash('We hope you enjoyed organizing and sharing lists see you soon')
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)