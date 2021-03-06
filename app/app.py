"""All routes and their actions"""

import os

from functools import wraps
from datetime import datetime
from flask import Flask, current_app, render_template, redirect, url_for, request, session, flash
from app.models.user import User
from app.models.store import Store
from app.models.shoppinglist import ShoppingList
from app.models.shoppinglistitem import ShoppingListItem
from werkzeug.security import generate_password_hash
from app.forms import RegisterForm, LoginForm, ListForm, EditList, ItemForm

app = Flask(__name__)
with app.app_context():
    # within this block, current_app points to app.
    current_app.name


app.config.from_object(os.environ['APP_SETTINGS'])

store = Store()


def login_required(f):
    """Allow some routes to be accessed only when logged_in"""

    @wraps(f)
    def wrap(*args, **kwargs):
        """Validate if the user is logged in before loading a route"""
        if 'logged_in' in session:
            return f(*args, **kwargs)
        flash('Please Log into your ShoppingList Account first')
        return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def home():
    """Render the homepage and Ensure a user can create an account"""

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
            # Validates user exists or is saved
            if 'id' not in session:
                user = new_user.save_user()
                if user != False:
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    session['user'] = request.form['email']
                    session['index'] = store.user_logged_in_index()
                    session['id'] = store.get_user_uuid()

                    flash('Welcome ' + session['username'])
                    return redirect(url_for('dashboard'))
                flash("User already exists")
                return render_template("homepage.html", form=form, error=error)
            flash("Another account is already in service")
            return render_template("homepage.html", form=form, error=error)
        return render_template("homepage.html", form=form, error=error)
    return render_template("homepage.html", form=form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render the login page and Ensure users can login"""

    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':

        if form.validate_on_submit():

            if store.check_login(request.form['username'], request.form['password']):

                session['logged_in'] = True
                session['user'] = request.form['username']
                session['index'] = store.user_logged_in_index()
                session['id'] = store.get_user_uuid()
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
    """Renders the dashboard and ensure a user can create his first shopping list"""

    error = None
    form = ListForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            get_id = session['id']
            new_shopping_list = ShoppingList(
                owner_id=get_id,
                title=request.form['title'],
                description=request.form['description'],
                created_on=datetime.now()
            )
            if new_shopping_list.save_list():
                flash('List created successfuly')
                return render_template(
                    "dashboard.html",
                    form=form,
                    data_item=store.shoppinglistitems,
                    data=store.get_user_lists()
                )
            flash("List already exists")
            return render_template(
                "dashboard.html",
                form=form,
                data=store.get_user_lists(),
                data_item=store.shoppinglistitems
            )
        return render_template(
            "dashboard.html",
            form=form,
            data=store.get_user_lists(),
            data_item=store.shoppinglistitems,
            error=error
        )
    return render_template(
        "dashboard.html",
        form=form,
        data=store.get_user_lists(),
        data_item=store.shoppinglistitems,
    )


@app.route('/edit-list/<list_id>', methods=['GET', 'POST'])
@login_required
def edit_list(list_id):
    """Allow a user to change a shopping list of his choice"""

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
            if renew_list.update_list() is True:
                flash('Shopping list updated successfuly')
                return redirect(url_for('dashboard'))
            flash(renew_list.update_list())
            return redirect(url_for('dashboard'))

    return render_template(
        "includes/edit_list.html",
        form=form,
        data=store.get_user_lists(),
        data_item=store.shoppinglistitems,
        form_data=serve_temp
    )


@app.route('/delete-list/<list_id>')
@login_required
def delete_list(list_id):
    """Allow a user to delete a list of his choice"""

    if store.delete_data('shoppinglist', list_id):
        flash("Shopping list deleted succesfully")
        return redirect(url_for('dashboard'))
    flash("Shopping list could not be found")
    return redirect(url_for('dashboard'))


@app.route('/add-item/<list_id>', methods=['GET', 'POST'])
@login_required
def add_shopping_item(list_id):
    """Allow a user to add an item to a shopping list"""

    form = ItemForm(request.form)
    error = None
    serve_shoppinglist = store.get_list_data(list_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_sl_item = ShoppingListItem(
                item_title=request.form['item_title'],
                item_description=request.form['item_description'],
                shoppinglist_id=list_id,
                created_on=datetime.now()
            )

            # Save the item to a shopping list relevant
            save_item = new_sl_item.save_sl_item()
            if save_item != False:
                flash("Item added successfuly")
                return redirect(url_for('dashboard'))
            flash("Item already exists")
            return redirect(url_for('dashboard'))
        return render_template(
            "dashboard.html",
            form=form,
            error=error,
            shoppinglistdata=serve_shoppinglist,
            to_load='add-item',
            data=store.get_user_lists()
        )
    return render_template(
        "dashboard.html",
        form=form,
        shoppinglistdata=serve_shoppinglist,
        to_load='add-item',
        data=store.get_user_lists()
    )


@app.route('/shoppinglists_items/<list_id>', methods=['GET', 'POST'])
@login_required
def get_shoppinglist_item(list_id):
    """Allow a user to view all items on a shopping list"""

    serve_shoppinglist = store.get_list_data(list_id)
    return render_template(
        "dashboard.html",
        form=ItemForm(request.form),
        shoppinglistdata=serve_shoppinglist,
        to_load='all-items',
        shoppinglistitems=store.get_shoppinglists_items(list_id),
        data=store.get_user_lists()
    )


@app.route('/update-shoppinglistitem/<item_id>', methods=['GET', 'POST'])
@login_required
def update_shoppinglist_item(item_id):
    """Allow a user to view all items on a shopping list"""

    form = ItemForm(request.form)
    serve_shoppinglistitem = store.get_item_data(item_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            renew_shoppinglistitem = ShoppingListItem(
                shoppinglist_id=serve_shoppinglistitem['shoppinglist_id'],
                item_title=request.form['item_title'],
                item_description=request.form['item_description'],
                item_id=item_id,
                created_on=request.form['item_created_on']
            )
            if renew_shoppinglistitem.update_shoppinglist_item():
                flash('Item on list updated successfuly')
                return render_template(
                    "dashboard.html",
                    form=form,
                    shoppinglistdata=store.get_list_data(
                        serve_shoppinglistitem['shoppinglist_id']
                    ),
                    to_load='all-items',
                    data=store.get_user_lists(),
                    shoppinglistitems=store.get_shoppinglists_items(
                        serve_shoppinglistitem['shoppinglist_id']
                        )
                )
            flash('Shopping List Item already exists')
            return render_template(
                "dashboard.html",
                form=form,
                shoppinglistdata=store.get_list_data(
                    serve_shoppinglistitem['shoppinglist_id']
                ),
                to_load='all-items',
                data=store.get_user_lists(),
                shoppinglistitems=store.get_shoppinglists_items(
                    serve_shoppinglistitem['shoppinglist_id']
                    )
            )
        flash("Invalid data to update Item")
        return render_template(
            "dashboard.html",
            form=form,
            shoppinglistdata=store.get_list_data(
                serve_shoppinglistitem['shoppinglist_id']
            ),
            to_load='all-items',
            data=store.get_user_lists(),
            shoppinglistitems=store.get_shoppinglists_items(
                    serve_shoppinglistitem['shoppinglist_id']
                    )
        )
    return render_template(
        "dashboard.html",
        form=form,
        shoppinglistdata=store.get_list_data(
            serve_shoppinglistitem['shoppinglist_id']
        ),
        to_load='all-items',
        data=store.get_user_lists(),
        shoppinglistitems=store.get_shoppinglists_items(
                    serve_shoppinglistitem['shoppinglist_id']
                    )
    )


@app.route('/delete_shoppinglistitem/<item_id>', methods=['GET', 'POST'])
@login_required
def delete_shoppinglist_item(item_id):
    """Allow a user to delete an item of his choice"""

    serve_shoppinglistitem = store.get_item_data(item_id)
    if store.delete_data('shoppinglistitem', item_id):
        flash("Item list deleted succesfully")
        return render_template(
            "dashboard.html",
            form=ItemForm(request.form),
            shoppinglistdata=store.get_list_data(
                serve_shoppinglistitem['shoppinglist_id']
            ),
            to_load='all-items',
            data=store.get_user_lists(),
            shoppinglistitems=store.get_shoppinglists_items(
                serve_shoppinglistitem['shoppinglist_id']
            )
        )
    flash("Shopping list could not be found")
    return render_template(
        "dashboard.html",
        form=ItemForm(request.form),
        shoppinglistdata=store.get_list_data(
            serve_shoppinglistitem['shoppinglist_id']
        ),
        to_load='all-items',
        data=store.get_user_lists(),
        shoppinglistitems=store.get_shoppinglists_items(
            serve_shoppinglistitem['shoppinglist_id']
        )
    )


@app.route('/logout')
@login_required
def logout():
    """Ensure a logged in user can logout of his account"""

    session.pop('logged_in', None)
    session.pop('user', None)
    session.pop('index', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('We hope you enjoyed organizing and sharing lists see you soon')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
