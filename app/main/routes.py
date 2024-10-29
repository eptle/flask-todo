from flask import render_template, url_for
from app import db
from app.main import bp
from flask_login import current_user, login_user, logout_user, \
    login_required
import sqlalchemy as sa



@bp.route('/')
@bp.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('main/index.html', title='main')
