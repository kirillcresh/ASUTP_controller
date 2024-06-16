from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class CurrentState(Base):
    __tablename__ = "current_state"
    __table_args__ = {'comment': 'This table stores current state data'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_id: Mapped[int] = mapped_column(
        ForeignKey("param.id"), nullable=False
    )
    element_id: Mapped[int] = mapped_column(
        ForeignKey("element.id"), nullable=False
    )
    value: Mapped[float] = mapped_column(Numeric(10, 2), comment="Значение показателя", nullable=False)
    update_time: Mapped[datetime] = mapped_column(DateTime, comment="Дата обновления записи", default=datetime.utcnow(), nullable=False)
