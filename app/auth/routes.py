from flask import redirect, render_template, flash, url_for, \
    request, jsonify
from app import db
from app.auth import bp
from app.auth.forms import RegistationForm, LoginForm
from flask_login import current_user, login_user, logout_user, \
    login_required
import sqlalchemy as sa
from app.models import User


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='login', form=form)


@bp.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data,
                        email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
    return render_template('auth/register.html', title='register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
