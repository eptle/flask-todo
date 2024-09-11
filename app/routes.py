from flask import redirect, render_template, flash, url_for
from app import app, db
from app.forms import RegistationForm, LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='main')


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='login', form=form)


@app.route('/register')
def register():
    form = RegistationForm()
    return render_template('register.html', title='registration', form=form)


@app.route('/<username>/boards')
def boards(username):
    return render_template('boards.html')
