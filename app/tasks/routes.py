from flask import redirect, render_template, url_for, \
    request, jsonify
from app import db
from app.tasks import bp
from app.tasks.forms import AddTaskForm, DeleteTaskForm
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.models import Task


@bp.route('/<username>/boards/<board_id>/<board_title>', methods=['POST', 'GET'])
@login_required
def tasks(username, board_id, board_title):
    if current_user.is_anonymous or current_user.username != username:
        return redirect(url_for('main.index'))

    add_task_form = AddTaskForm()
    delete_task_form = DeleteTaskForm()
    if add_task_form.validate_on_submit():
        new_task = Task(board_id=board_id, title=add_task_form.title.data,
                         position=Task.get_position(board_id))
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(url_for(
            'tasks.tasks',
            username=current_user.username,
            board_id=board_id,
            board_title=board_title
        ))

    query = sa.select(Task).where(Task.board_id == board_id)
    tasks = db.session.scalars(query).all()
    tasks_dicts = [t.to_dict() for t in tasks]
    tasks_dicts.sort(key=lambda x: x['position'])

    return render_template(
        'tasks/todolist.html',
        username=username,
        board_id=board_id,
        board_title=board_title,
        add_task_form=add_task_form,
        delete_task_form=delete_task_form,
        tasks=tasks_dicts,
        title=board_title
    )


@bp.route('/delete-task/<task_id>', methods=['POST', 'GET'])
@login_required
def delete_task(task_id):
    task = db.session.scalar(sa.select(Task).where(Task.id == task_id))
    query = db.session.query(Task).filter_by(id=task_id).first()
    board_id = query.board_id
    board_title = query.board.title

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('tasks.tasks', username=current_user.username, board_id=board_id, board_title=board_title))


@bp.route('/update-task-order', methods=['POST'])
@login_required
def update_task_order():
    task_order = request.json

    try:
        for task_data in task_order:
            task = db.session.query(Task).get(task_data['id'])
            if task:
                task.position = task_data['position']
        db.session.commit()
        return jsonify({'status': 'success'})
    
    except Exception as e:
        db.session.rollback()
        print(f'Error {e}')
        return jsonify({'status': 'error'}), 500


@bp.route('/edit-task', methods=['GET', 'POST'])
@login_required
def edit_task():
    new_task_name = request.json
    
    try:
        task = db.session.query(Task).get(new_task_name['task_id'])
        if task:
            task.title = new_task_name['new_title']
        db.session.commit()
        return jsonify({'status': 'success'})

    except Exception as e:
        db.session.rollback()
        print(f'Error {e}')
        return jsonify({'status': 'error'}), 500
