"""this module handles the field defination of registration and bucketlist creation"""
from flask_wtf import Form
from wtforms import TextField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(Form):
    username = TextField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = TextField(
        'Email',
        validators=[DataRequired(), Email(message=None), Length(min=3, max=25)]
    )    
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    confirmpassword = PasswordField(
        'ConfirmPassword',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )