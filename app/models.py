from app import app, db
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(50) ,unique=True)
    email: Mapped[str] = mapped_column(sa.String(100), unique=True)
    password: Mapped[str] = mapped_column(sa.String(100))
    date_joined: Mapped[datetime] = mapped_column(sa.Date)
    