from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from database import Base

from .element_model import Element
from .param_model import Param


class StateRegister(Base):
    __tablename__ = "state_register"
    __table_args__ = {"comment": "This table stores state register data"}

    id = Column(Integer, primary_key=True)
    param_id = Column(Integer, ForeignKey("param.id"), nullable=False)
    element_id = Column(Integer, ForeignKey("element.id"), nullable=False)
    value = Column(Numeric(10, 3), comment="Значение показателя", nullable=False)
    date_created = Column(
        DateTime,
        comment="Дата создания записи",
        default=datetime.utcnow,
        nullable=False,
    )
    param = relationship(Param, backref="state_register")
    element = relationship(Element, backref="state_register")
