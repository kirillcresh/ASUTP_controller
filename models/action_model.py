from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Action(Base):
    __tablename__ = "action"
    __table_args__ = {'comment': 'This table stores action names'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, comment="Название действия", nullable=False)
