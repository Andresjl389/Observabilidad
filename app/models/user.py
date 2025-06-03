import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.db import Base


from models.info import Info
from models.token import Token
from models.type_info import Type
from models.role import Role

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role_id = Column(Uuid, ForeignKey("role.id"))
    password = Column(String, nullable=False)

    token = relationship("Token", back_populates="user")
    info = relationship("Info", back_populates="user")
    role = relationship("Role", back_populates="user")