"""All the forms for user registration, login, create list/item,
edit list/item are validated here"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """Implement the login form"""

    username = TextField('Username', validators=[
        DataRequired(),
        Email(message=None)
    ])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    """Implement the register form"""

    username = TextField(
        'Username',
        validators=[DataRequired(), Length(min=5, max=50)]
    )
    email = TextField(
        'Email',
        validators=[DataRequired(), Email(message=None),
                    Length(min=10, max=50)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=5, max=50)]
    )
    confirmpassword = PasswordField(
        'ConfirmPassword',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )


class ListForm(FlaskForm):
    """Implement the add shopping list form"""

    title = TextField('Title', validators=[
        DataRequired(),
        Length(min=8, max=100)
    ])
    description = TextAreaField('Content', validators=[
        DataRequired(),
        Length(max=250)
    ])


class ItemForm(FlaskForm):
    """Implement the add item on shopping list form"""

    item_title = TextField('Item_Title', validators=[
        DataRequired(),
        Length(min=8, max=100)
    ])
    item_description = TextAreaField(
        'Item_Description', validators=[Length(max=250)])
    item_created_on = HiddenField('Created_On')


class EditList(FlaskForm):
    """Implement the edit shopping list item form"""

    title = TextField('Title', validators=[
        DataRequired(),
        Length(min=8, max=100)
    ])
    description = TextAreaField('Content', validators=[
        DataRequired(),
        Length(max=250)
    ])
    hidden = HiddenField('Hidden')
