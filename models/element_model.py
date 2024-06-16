from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Element(Base):
    __tablename__ = "element"
    __table_args__ = {"comment": "This table stores elements data"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        Text, comment="Название показателя", nullable=False
    )
