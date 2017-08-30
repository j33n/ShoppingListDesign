# """ module for the routes and views """
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from models.user import User
from models.store import Store
from models.shoppinglist import ShoppingList
from werkzeug.security import generate_password_hash, \
     check_password_hash
from datetime import datetime
from forms import RegisterForm, LoginForm, ListForm

app = Flask(__name__)

# Configurations
app.secret_key = "&\xb2\xc8\x80^H\xef\xb7\xc9\xb11\\\xf0\xe5}\xdd\xb8[O\x0b\tK\x0e\xbe"

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
	print(session['storage'])
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
			session['logged_in'] = True
			Store().store_session([new_user.user_data()])
			flash(
				'Welcome ' + session['storage']
				[len(session['storage'])-1]
				['username']
			)
			return redirect(url_for('dashboard'))
		return render_template("homepage.html", form=form, error=error)
	return render_template("homepage.html", form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			if(request.form['username'] != session['storage']['email'])\
				or check_password_hash(
					session['storage']['password'], request.form['password']) is False:
				error = 'Invalid Credentials, Try Again'
			else:
				session['logged_in'] = True
				flash('Welcome back ' + session['storage']['username'])
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
				owner_id=session['storage']['user_id'],
				title=request.form['title'],
				description=request.form['description'],
				created_on=datetime.now()
			)
			Store().newlist_session(new_list.list_data())			
			flash('List created successfuly')
			return render_template("dashboard.html", form=form)
		flash('Something went wrong')
		return render_template("dashboard.html", form=form)
	return render_template("dashboard.html", form=form)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('We hope you enjoyed organizing and sharing lists see you soon')
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)