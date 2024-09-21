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

    board: Mapped[list['Board']] = relationship('Board', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    

class Board(db.Model):
    __tablename__ = 'board'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'), index=True)
    title: Mapped[str] = mapped_column(sa.String(50))
    date_created: Mapped[datetime] = mapped_column(sa.Date, default=lambda: datetime.now(timezone.utc))
    position: Mapped[int] = mapped_column()

    user: Mapped['User'] = relationship('User', back_populates='board')
    task: Mapped[list['Task']] = relationship('Task', 
                                                back_populates='board',
                                                cascade="all, delete-orphan"
                                                )

    __table_args__ = (sa.UniqueConstraint('user_id', 'position', name='user_position_uc'),)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'position': self.position,
            'user_id': self.user_id
        }
    
    @staticmethod
    def get_position(current_user):
        max_position = db.session.query(sa.func.max(Board.position)).filter_by(user_id = current_user.id).scalar()
        new_position = 1 if max_position is None else max_position + 1
        return new_position
    

class Task(db.Model):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    board_id: Mapped[int] = mapped_column(sa.ForeignKey('board.id'), index=True)
    title: Mapped[str] = mapped_column(sa.String(50))
    position: Mapped[int] = mapped_column()
    last_edit: Mapped[datetime] = mapped_column(sa.Date, default=lambda: datetime.now(timezone.utc))

    board: Mapped["Board"] = relationship("Board", back_populates="task")

    def to_dict(self):
        return {
            'id': self.id,
            'board_id': self.board_id,
            'title': self.title,
            'position': self.position
        }
    
    @staticmethod
    def get_position(board_id):
        max_position = db.session.query(sa.func.max(Task.position)).filter_by(board_id = board_id).scalar()
        new_position = 1 if max_position is None else max_position + 1
        return new_position
    

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))