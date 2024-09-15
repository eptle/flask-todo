from flask import redirect, render_template, flash, url_for, request
from app import app, db, login
from app.forms import RegistationForm, LoginForm, AddBoardForm, \
    AddTaskForm, DeleteForm, EditForm, OpenForm
from flask_login import current_user, login_user, logout_user, \
    login_required
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


@app.route('/<username>/boards', methods=['POST', 'GET'])
@login_required
def boards(username):
    if current_user.is_anonymous or current_user.username != username:
        return redirect(url_for('index'))

    open_board_form = OpenForm()
    delete_board_form = DeleteForm()
    edit_board_form = EditForm()

    add_board_form = AddBoardForm()
    if add_board_form.validate_on_submit():
        new_board = Boards(title=add_board_form.title.data, user_id=current_user.id, position=Boards.get_position(current_user))
        db.session.add(new_board)
        db.session.commit()
        return redirect(url_for('boards', username=current_user.username))

    query = sa.select(Boards).where(Boards.user_id == current_user.id)
    user_boards = db.session.scalars(query).all()
    board_dicts = [b.to_dict() for b in user_boards]
    is_board = True # переменная для тега <title>
    return render_template(
        'boards.html', 
        is_board=is_board, 
        form=add_board_form, 
        boards=board_dicts,
        open_board_form=open_board_form,
        delete_board_form=delete_board_form,
        edit_board_form=edit_board_form,
        title='Boards'
        )


@app.route('/delete-board', methods=['POST', 'GET'])
@login_required
def delete_board():
    board_id = request.form.get('board_id')
    board = db.session.scalar(sa.select(Boards).where(Boards.id == board_id))

    if board:
        db.session.delete(board)
        db.session.commit()
    else:
        flash("I can't delete this, sorry :(", 'danger')

    return redirect(url_for('boards', username=current_user.username))


@app.route('/<username>/boards/<board_id>/<board_title>', methods=['POST', 'GET'])
@login_required
def tasks(username, board_id, board_title):
    if current_user.is_anonymous or current_user.username != username:
        return redirect(url_for('index'))

    form = AddTaskForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'tasks', username=current_user.username, 
            board_id=board_id, 
            board_title=board_title
            ))

    return render_template(
        'todolist.html', 
        username=username, 
        board_id=board_id, 
        board_title=board_title,
        form=form,
        title=board_title
        )


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(e):
    return render_template('errors/403.html'), 403


@app.route('/favicon.ico')
def favicon():
    return 'CHINCHIN', 204