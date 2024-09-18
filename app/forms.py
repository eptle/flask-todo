from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, EmailField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app import db
import sqlalchemy as sa
from app.models import User
from markupsafe import Markup


# authentication forms
class RegistationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=8, max=80)])
    password2 = PasswordField('Repeat password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(
            sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username')
        
    def validate_username(self, email):
        email = db.session.scalar(
            sa.select(User).where(User.email == email.data))
        if email is not None:
            raise ValidationError('Please use a different username')


class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


# board forms
class AddBoardForm(FlaskForm):
    title = StringField('Board name: ', validators=[DataRequired()])
    submit = SubmitField('Create')

    # def validate_board_name(self, name):
    #     board = db.session.scalar()


class OpenBoardForm(FlaskForm):
    submit = SubmitField('Open', render_kw={'class': 'board-btn open-board'})


class DeleteBoardForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={'class': 'board-btn delete-board'})


# task forms
class AddTaskForm(FlaskForm):
    title = StringField('', validators=[DataRequired()])
    submit = SubmitField('Add task', render_kw={'class': 'board-btn add-task'})


class DeleteTaskForm(FlaskForm):
    submit = SubmitField('', render_kw={'class': 'board-btn task-done'})
