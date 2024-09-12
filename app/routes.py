from flask import redirect, render_template, flash, url_for
from app import app, db, login
from app.forms import RegistationForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Boards, Tasks


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html', title='main')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='login', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/<username>/boards')
def boards(username):
    is_board = True # переменная для тега <title>
    if current_user.username != username:
        return redirect(url_for('index'))
    return render_template('boards.html', is_board=is_board)


@login_required
@app.route('/<username>/boards/<board_name>', method=['POST', 'GET'])
def tasks(username):
    is_board = False # переменная для тега <title>
    if current_user.username != username:
        return redirect(url_for('index'))
    return render_template('boards.html', is_board=is_board)