from sqlalchemy import Column, Integer, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class RoleEnum(str, enum.Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    role = Column(Enum(RoleEnum), nullable=False)

    user = relationship("User", back_populates="permissions")
    event = relationship("Event", back_populates="permissions")

    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='uix_user_event'),)
