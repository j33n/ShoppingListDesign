"""this module handles the field defination of registration and bucketlist creation"""
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, validators, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired()])
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
    title = TextField('Title', validators=[DataRequired()])
    description = TextAreaField('Content', validators=[DataRequired(), Length(max=225)])

class EditList(FlaskForm):
    title = TextField('Title', validators=[DataRequired()])
    description = TextAreaField('Content', validators=[DataRequired(), Length(max=225)])
    hidden = HiddenField('Hidden')