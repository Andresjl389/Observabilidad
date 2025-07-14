import uuid
from sqlalchemy import Column, String, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Info(Base):
    __tablename__ = "info"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    filename = Column(String, index=True)
    filepath = Column(String, index=True)
    icon = Column(String, index=True)
    link = Column(String, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    type_id = Column(Uuid, ForeignKey("type.id"))


    user = relationship("User", back_populates="info")
    type = relationship("Type", back_populates="info")
