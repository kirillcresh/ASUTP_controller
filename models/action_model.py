from sqlalchemy import Column, Integer, Text

from database import Base


class Action(Base):
    __tablename__ = "action"
    __table_args__ = {"comment": "This table stores action names"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, comment="Название действия", nullable=False)
