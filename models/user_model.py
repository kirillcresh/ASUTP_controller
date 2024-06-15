from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'comment': 'This table stores user data'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), comment="Имя пользователя")
    login: Mapped[str] = mapped_column(String(32), comment="Логин", unique=True)
    password: Mapped[str] = mapped_column(String(64), comment="Пароль")
