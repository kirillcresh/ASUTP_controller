from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from database import Base


class Error(Base):
    __tablename__ = "error"
    __table_args__ = {"comment": "This table stores errors data"}

    id = Column(Integer, primary_key=True)
    error_text = Column(Text, comment="Текст ошибки", nullable=False)
    closed_by = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    date_created = Column(
        DateTime,
        comment="Дата получения сообщения об ошибке",
        default=datetime.utcnow,
        nullable=False,
    )
