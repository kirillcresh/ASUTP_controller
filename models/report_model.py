from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from database import Base


class Report(Base):
    __tablename__ = "report"
    __table_args__ = {"comment": "This table stores reports data"}

    id = Column(Integer, primary_key=True)
    created_by = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    filename = Column(Text, comment="Имя отчета", nullable=False)
    date_created = Column(
        DateTime,
        comment="Дата создания отчета",
        default=datetime.utcnow,
        nullable=False,
    )
    user = relationship("User", backref="report")
