from flask import redirect, render_template, flash, url_for, \
    request, jsonify
from app import app, db, login
from app.forms import RegistationForm, LoginForm, \
    AddBoardForm, DeleteBoardForm, EditBoardForm, OpenBoardForm, \
    AddTaskForm, DeleteTaskForm, EditTaskForm
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

    open_board_form = OpenBoardForm()
    delete_board_form = DeleteBoardForm()
    edit_board_form = EditBoardForm()

    add_board_form = AddBoardForm()
    if add_board_form.validate_on_submit():
        new_board = Boards(title=add_board_form.title.data,
                           user_id=current_user.id, position=Boards.get_position(current_user))
        db.session.add(new_board)
        db.session.commit()
        return redirect(url_for('boards', username=current_user.username))

    query = sa.select(Boards).where(Boards.user_id == current_user.id)
    user_boards = db.session.scalars(query).all()
    board_dicts = [b.to_dict() for b in user_boards]
    is_board = True  # переменная для тега <title>
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


@app.route('/delete-board/<board_id>', methods=['POST', 'GET'])
@login_required
def delete_board(board_id):
    board = db.session.scalar(sa.select(Boards).where(Boards.id == board_id))

    db.session.delete(board)
    db.session.commit()

    return redirect(url_for('boards', username=current_user.username))


@app.route('/<username>/boards/<board_id>/<board_title>', methods=['POST', 'GET'])
@login_required
def tasks(username, board_id, board_title):
    if current_user.is_anonymous or current_user.username != username:
        return redirect(url_for('index'))

    add_task_form = AddTaskForm()
    delete_task_form = DeleteTaskForm()
    if add_task_form.validate_on_submit():
        new_task = Tasks(board_id=board_id, title=add_task_form.title.data,
                         position=Tasks.get_position(board_id))
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(url_for(
            'tasks',
            username=current_user.username,
            board_id=board_id,
            board_title=board_title
        ))

    query = sa.select(Tasks).where(Tasks.board_id == board_id)
    tasks = db.session.scalars(query).all()
    tasks_dicts = [t.to_dict() for t in tasks]
    print(tasks_dicts)

    return render_template(
        'todolist.html',
        username=username,
        board_id=board_id,
        board_title=board_title,
        add_task_form=add_task_form,
        delete_task_form=delete_task_form,
        tasks=tasks_dicts,
        title=board_title
    )


@app.route('/delete-task/<task_id>', methods=['POST', 'GET'])
@login_required
def delete_task(task_id):
    task = db.session.scalar(sa.select(Tasks).where(Tasks.id == task_id))
    query = db.session.query(Tasks).filter_by(id=task_id).first()
    board_id = query.board_id
    board_title = query.board.title

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('tasks', username=current_user.username, board_id=board_id, board_title=board_title))


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(e):
    return render_template('errors/403.html'), 403


@app.route('/favicon.ico')
def favicon():
    return 'CHINCHIN', 204
