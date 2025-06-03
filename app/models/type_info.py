import uuid
from sqlalchemy import Column, String, Uuid
from sqlalchemy.orm import relationship
from core.db import Base

from models.info import Info


class Type(Base):
    __tablename__ = "type"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    name = Column(String, index=True, nullable= False)

    info = relationship("Info", back_populates="type")
