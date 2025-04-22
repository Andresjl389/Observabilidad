import uuid
from sqlalchemy import Column, String, Uuid
from sqlalchemy.orm import relationship
from core.db import Base



class Role(Base):
    __tablename__ = "role"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    name = Column(String, index=True, nullable= False)

    user = relationship("User", back_populates="role")
