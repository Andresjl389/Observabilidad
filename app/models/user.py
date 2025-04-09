import uuid
from sqlalchemy import Column, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.db import Base


from models.info import Info
from models.token import Token
from models.type_info import Type

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)

    token = relationship("Token", back_populates="user")
    info = relationship("Info", back_populates="user")