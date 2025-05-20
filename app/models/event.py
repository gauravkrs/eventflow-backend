from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="events")
    permissions = relationship("Permission", back_populates="event", cascade="all, delete")
    versions = relationship("EventVersion", back_populates="event", cascade="all, delete")
    changelogs = relationship("Changelog", back_populates="event", cascade="all, delete")
