from app import app, db
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, WriteOnlyMapped, relationship, registry
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(50) ,unique=True, index=True)
    email: Mapped[str] = mapped_column(sa.String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(sa.String(100))
    date_joined: Mapped[datetime] = mapped_column(sa.Date, default=lambda: datetime.now(timezone.utc))

    boards: Mapped[list['Boards']] = relationship('Boards', back_populates='user')
    

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


