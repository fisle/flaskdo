# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, session, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm, SignupForm, TodoForm
from models import User, Todo
from flask.ext.bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@lm.user_loader
def load_user(user_id):
  user_id = User.query.get(user_id)
  return user_id

@app.before_request
def before_request():
  g.user = current_user

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
  form = TodoForm()
  if form.validate_on_submit():
    todo = Todo(subject = form.subject.data, priority = form.priority.data, user = g.user.id, deadline = form.deadline.data)
    db.session.add(todo)
    db.session.commit()
    redirect(url_for('index'))
  todo = Todo.query.filter_by(user = g.user.id).order_by(Todo.priority.desc()).all()
  return render_template('index.html', todo = todo, form = form)

@app.route('/delete/<int:id>/')
@login_required
def delete(id):
  todo = Todo(id = id, user = g.user.id)
  Todo.query.filter_by(id = id, user = g.user.id).delete()
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/done/<int:id>/')
@login_required
def done(id):
  todo = Todo(id = id, user = g.user.id, priority = 0)
  db.session.merge(todo)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
  if g.user is not None and g.user.is_authenticated():
    flash('Already registered.')
    return redirect(url_for('index'))
  form = SignupForm()
  if form.validate_on_submit():
    user = User(username = form.username.data, password = bcrypt.generate_password_hash(form.password.data))
    db.session.add(user)
    db.session.commit()
    flash('Account created! You are now logged in!')
    login_user(user)
    return redirect(url_for('index'))
  return render_template('signup.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
  if g.user is not None and g.user.is_authenticated():
    flash('Already logged in.')
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data
    user = form.username.data
    user_data = User.query.filter_by(username = user).first()
    if user_data:
      if bcrypt.check_password_hash(user_data.password, form.password.data):
        if 'remember_me' in session:
          remember_me = session['remember_me']
          session.pop('remember_me', None)
        login_user(user_data, remember = remember_me)
        flash('Logged in!')
        return redirect(request.args.get('next') or url_for('index'))
      else:
        flash('Invalid username or password')
    else:
      flash('Invalid username or password')
  return render_template('login.html', form = form)

@app.route('/logout')
def logout():
  logout_user()
  flash('Logged out!')
  return redirect(url_for('index'))
