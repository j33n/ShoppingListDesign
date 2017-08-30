# """ module for the routes and views """
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import json
from models.user import User
from werkzeug.security import generate_password_hash
from models.store import Store
from datetime import datetime
from forms import RegisterForm, LoginForm

app = Flask(__name__)

# Configurations
app.secret_key = "&\xb2\xc8\x80^H\xef\xb7\xc9\xb11\\\xf0\xe5}\xdd\xb8[O\x0b\tK\x0e\xbe"

@app.route('/', methods=['GET', 'POST'])
def home():
	error = None
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(
				username=request.form['username'],
				email=request.form['email'],
				password=request.form['password'],
				created_on=datetime.now()
			)
			session['logged_in'] = True
			session['current'] = new_user.user_data()
			flash('Welcome ' + session['current']['username'])
			return redirect(url_for('dashboard'))
		return render_template("homepage.html", form=form, error=error)
	return render_template("homepage.html", form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			if(request.form['username'] != 'admin')\
				or request.form['password'] != 'admin':
				error = 'Invalid Credentials, Try Again'
			else:
				session['logged_in'] = True
				session['username'] = request.form['username']
				flash('Welcome ' + session['username'])
				return redirect(url_for('dashboard'))
		else:
			return render_template("login.html", form=form, error=error)
	return render_template("login.html", form=form, error=error)

@app.route('/dashboard')
def dashboard():
	return render_template("dashboard.html")

@app.route('/logout')
def logout():
	# session.pop('logged_in', None)
	# session.pop('username', None)
	session.clear()
	flash('We hope you enjoyed organizing and sharing list see you soon')
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)