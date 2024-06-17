from sqlalchemy import Column, Integer, Text

from database import Base


class Element(Base):
    __tablename__ = "element"
    __table_args__ = {"comment": "This table stores elements data"}

    id = Column(Integer, primary_key=True)
    name = Column(Text, comment="Название показателя", nullable=False)
