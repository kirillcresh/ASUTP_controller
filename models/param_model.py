from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Param(Base):
    __tablename__ = "param"
    __table_args__ = {"comment": "This table stores params data"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dimension: Mapped[str] = mapped_column(
        Text, comment="Название единицы измерения", nullable=False
    )
    name: Mapped[str] = mapped_column(
        Text, comment="Название показателя", nullable=False
    )
    type: Mapped[int] = mapped_column(
        Integer, comment="Тип параметра", default=1, nullable=False
    )
