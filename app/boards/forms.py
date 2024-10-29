from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, EmailField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app import db
import sqlalchemy as sa
from app.models import User
from markupsafe import Markup


class AddBoardForm(FlaskForm):
    title = StringField('Board name: ', validators=[DataRequired()])
    submit = SubmitField('Create')

    # def validate_board_name(self, name):
    #     board = db.session.scalar()


class OpenBoardForm(FlaskForm):
    submit = SubmitField('Open', render_kw={'class': 'board-btn open-board'})


class DeleteBoardForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={'class': 'board-btn delete-board'})
