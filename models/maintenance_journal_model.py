from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship

from database import Base


class MaintenanceJournal(Base):
    __tablename__ = "maintenance_journal"
    __table_args__ = {"comment": "This table stores maintenance journal data"}

    id = Column(Integer, primary_key=True)
    action_id = Column(
        Integer, ForeignKey("action.id", ondelete="CASCADE"), nullable=False
    )
    created_by = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(Text, comment="Описание действия", nullable=False)
    value = Column(
        Numeric(10, 3), comment="Значение показателя, если валидно", nullable=True
    )
    date_created = Column(
        DateTime,
        comment="Дата создания записи",
        default=datetime.utcnow,
        nullable=False,
    )

    action = relationship("Action", backref="maintenance_journal")
    user = relationship("User", backref="maintenance_journal")
