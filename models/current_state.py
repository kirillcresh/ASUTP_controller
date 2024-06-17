from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric

from database import Base


class CurrentState(Base):
    __tablename__ = "current_state"
    __table_args__ = {"comment": "This table stores current state data"}

    id = Column(Integer, primary_key=True)
    param_id = Column(Integer, ForeignKey("param.id"), nullable=False)
    element_id = Column(Integer, ForeignKey("element.id"), nullable=False)
    value = Column(Numeric(10, 3), comment="Значение показателя", nullable=False)
    update_time = Column(
        DateTime,
        comment="Дата обновления записи",
        default=datetime.utcnow,
        nullable=False,
    )
