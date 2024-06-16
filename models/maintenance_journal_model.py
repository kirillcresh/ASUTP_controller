from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class MaintenanceJournal(Base):
    __tablename__ = "maintenance_journal"
    __table_args__ = {'comment': 'This table stores maintenance journal data'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_id: Mapped[int] = mapped_column(
        ForeignKey("action.id", ondelete="CASCADE"), nullable=False
    )
    created_by: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, comment="Описание действия", nullable=False)
    value: Mapped[float] = mapped_column(Numeric(10, 2), comment="Значение показателя, если валидно", nullable=True)
    date_created: Mapped[datetime] = mapped_column(DateTime, comment="Дата создания записи", default=datetime.utcnow(), nullable=False)

