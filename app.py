from flask import Flask, render_template, redirect, url_for, flash

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("homepage.html")

@app.route('/dashboard')
def dashboard():
	return render_template("dashboard.html")

@app.route('/login')
def login():
	return render_template("login.html")

@app.route('/explore')
def explore():
	return render_template("explore.html")

if __name__ == '__main__':
	app.run()