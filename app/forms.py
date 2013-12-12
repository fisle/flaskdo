from flask.ext.wtf import Form
from app import db
from wtforms import TextField, PasswordField, validators, SelectField, BooleanField, DateTimeField
from wtforms.validators import Required, EqualTo, Length
from app.models import User

def validate_user(form, field):
  if db.session.query(User).filter_by(username=form.username.data).count() > 0:
    raise validators.ValidationError('Username already exists')

def validate_email(form, field):
  if db.session.query(User).filter_by(email=form.email.data).count() > 0:
    raise validators.ValidationError('Email already in use')

class LoginForm(Form):
  username = TextField('username', validators = [Required(message='Please enter username')])
  password = PasswordField('password', validators = [Required(message='Please enter password')])
  remember_me = BooleanField('remember_me', default = False)

class SignupForm(Form):
  username = TextField('username', validators = [Required(), validate_user])
  password = PasswordField('password', [
    Required(message='Password cannot be empty'),
    EqualTo('confirm', message='Passwords did not match'),
    Length(min=8, max=100, message='Password too short')
  ])
  confirm = PasswordField('Repeat password', validators = [Required()])

class TodoForm(Form):
  subject = TextField('subject', validators = [Required()])
  priority = SelectField('priority', validators = [Required()], choices=[('1', 'Low'), ('2', 'Normal'), ('3', 'High')])
  deadline = DateTimeField('deadline', format = '%d.%m.%Y %H:%M')
