from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"comment": "This table stores user data"}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), comment="Имя пользователя", nullable=False)
    login = Column(String(32), comment="Логин", unique=True, nullable=False)
    password = Column(String(64), comment="Пароль", nullable=False)
    is_admin = Column(Boolean, comment="Администратор", default=False)
    refresh_token = Column(String(256), nullable=True)
