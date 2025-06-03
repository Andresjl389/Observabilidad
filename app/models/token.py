import uuid
from sqlalchemy import Column, String, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Token(Base):
    __tablename__ = "token"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    title = Column(String, index=True, nullable= False)
    token = Column(String, index=True,nullable= False )
    user_id = Column(Uuid, ForeignKey("users.id"))

    user = relationship("User", back_populates="token")