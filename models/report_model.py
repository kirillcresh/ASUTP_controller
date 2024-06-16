from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Report(Base):
    __tablename__ = "report"
    __table_args__ = {"comment": "This table stores reports data"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    filename: Mapped[str] = mapped_column(Text, comment="Имя отчета", nullable=False)
    date_created: Mapped[datetime] = mapped_column(
        DateTime,
        comment="Дата создания отчета",
        default=datetime.utcnow(),
        nullable=False,
    )
