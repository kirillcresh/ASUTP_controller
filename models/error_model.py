from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Error(Base):
    __tablename__ = "error"
    __table_args__ = {"comment": "This table stores errors data"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    error_text: Mapped[str] = mapped_column(
        Text, comment="Текст ошибки", nullable=False
    )
    closed_by: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    date_created: Mapped[datetime] = mapped_column(
        DateTime,
        comment="Дата получения сообщения об ошибке",
        default=datetime.utcnow(),
        nullable=False,
    )
