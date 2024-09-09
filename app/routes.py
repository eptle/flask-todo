from flask import redirect, render_template, flash, url_for
from app import app


@app.route('/')
@app.route('/index')
def index():
    title = 'Main'
    username = 'Eptel'
    return render_template('index.html', title=title, username=username)


@app.route()