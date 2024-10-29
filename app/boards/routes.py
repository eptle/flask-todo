from flask import redirect, render_template, url_for, \
    request, jsonify
from app import db
from app.boards import bp
from app.boards.forms import AddBoardForm, DeleteBoardForm, OpenBoardForm
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.models import Board


@bp.route('/<username>/boards', methods=['POST', 'GET'])
@login_required
def boards(username):
    if current_user.is_anonymous or current_user.username != username:
        return redirect(url_for('main.index'))

    open_board_form = OpenBoardForm()
    delete_board_form = DeleteBoardForm()

    add_board_form = AddBoardForm()
    if add_board_form.validate_on_submit():
        new_board = Board(title=add_board_form.title.data,
                           user_id=current_user.id, position=Board.get_position(current_user))
        db.session.add(new_board)
        db.session.commit()
        return redirect(url_for('boards.boards', username=current_user.username))

    query = sa.select(Board).where(Board.user_id == current_user.id)
    user_boards = db.session.scalars(query).all()
    board_dicts = [b.to_dict() for b in user_boards]
    is_board = True  # переменная для тега <title>
    return render_template(
        'boards/boards.html',
        is_board=is_board,
        form=add_board_form,
        boards=board_dicts,
        open_board_form=open_board_form,
        delete_board_form=delete_board_form,
        title='Boards'
    )


@bp.route('/delete-board/<board_id>', methods=['POST', 'GET'])
@login_required
def delete_board(board_id):
    board = db.session.scalar(sa.select(Board).where(Board.id == board_id))

    db.session.delete(board)
    db.session.commit()

    return redirect(url_for('boards.boards', username=current_user.username))


@bp.route('/edit-board', methods=['GET', 'POST'])
@login_required
def edit_board():
    new_board_name = request.json
    
    try:
        board = db.session.query(Board).get(new_board_name['board_id'])
        print('awdaddawdawdawd')
        if board:
            board.title = new_board_name['new_title']
        db.session.commit()
        return jsonify({'status': 'success'})

    except Exception as e:
        db.session.rollback()
        print(f'Error {e}')
        return jsonify({'status': 'error'}), 500
    