from app import app, db, login
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, WriteOnlyMapped, relationship, registry
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(50) ,unique=True, index=True)
    email: Mapped[str] = mapped_column(sa.String(100), unique=True, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(sa.String(256))
    date_joined: Mapped[datetime] = mapped_column(sa.Date, default=lambda: datetime.now(timezone.utc))

    boards: Mapped[list['Boards']] = relationship('Boards', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    

class Boards(db.Model):
    __tablename__ = 'boards'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'), index=True)
    name: Mapped[str] = mapped_column(sa.String(50))
    date_created: Mapped[datetime] = mapped_column(sa.Date, default=lambda: datetime.now(timezone.utc))

    user: Mapped['User'] = relationship('User', back_populates='boards')
    tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='board')


class Tasks(db.Model):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    board_id: Mapped[int] = mapped_column(sa.ForeignKey('boards.id'), index=True)
    title: Mapped[str] = mapped_column(sa.String(50))
    description: Mapped[str] = mapped_column(sa.String())
    position: Mapped[str] = mapped_column(unique=True)
    last_edit: Mapped[datetime] = mapped_column(sa.Date, default=lambda: datetime.now(timezone.utc))

    board: Mapped["Boards"] = relationship("Boards", back_populates="tasks")


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))