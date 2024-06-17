from sqlalchemy import Column, Integer, Text

from database import Base


class Param(Base):
    __tablename__ = "param"
    __table_args__ = {"comment": "This table stores params data"}

    id = Column(Integer, primary_key=True)
    dimension = Column(Text, comment="Название единицы измерения", nullable=False)
    name = Column(Text, comment="Название показателя", nullable=False)
    type = Column(Integer, comment="Тип параметра", default=1, nullable=False)
