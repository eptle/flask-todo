from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, EmailField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app import db
import sqlalchemy as sa
from app.models import User
from markupsafe import Markup


class AddTaskForm(FlaskForm):
    title = StringField('', validators=[DataRequired()])
    submit = SubmitField('Add task', render_kw={'class': 'board-btn add-task'})


class DeleteTaskForm(FlaskForm):
    submit = SubmitField('', render_kw={'class': 'board-btn task-done'})
