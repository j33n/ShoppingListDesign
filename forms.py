"""All the forms for user registration, login, create list/item,
edit list/item are validated here"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired(), Email(message=None)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = TextField(
        'Username',
        validators=[DataRequired(), Length(min=5, max=25)]
    )
    email = TextField(
        'Email',
        validators=[DataRequired(), Email(message=None), Length(min=10, max=25)]
    )    
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=5, max=25)]
    )
    confirmpassword = PasswordField(
        'ConfirmPassword',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )

class ListForm(FlaskForm):
    title = TextField('Title', validators=[DataRequired(), Length(min=8, max=100)])
    description = TextAreaField('Content', validators=[DataRequired(), Length(max=225)])

class ItemForm(FlaskForm):
    item_title = TextField('Item_Title', validators=[DataRequired(), Length(min=8, max=100)])
    item_description = TextAreaField('Item_Description', validators=[Length(max=225)])
    item_created_on = HiddenField('Created_On')

class EditList(FlaskForm):
    title = TextField('Title', validators=[DataRequired(), Length(min=8, max=100)])
    description = TextAreaField('Content', validators=[DataRequired(), Length(max=225)])
    hidden = HiddenField('Hidden')