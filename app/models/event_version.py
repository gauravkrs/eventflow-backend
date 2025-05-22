from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from app.db.base import Base

class EventVersion(Base):
    __tablename__ = "event_versions"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    version_number = Column(Integer, nullable=False)
    version_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    previous_version_id = Column(Integer, ForeignKey("event_versions.id"), nullable=True)

    event = relationship("Event", back_populates="versions")
    created_by_user = relationship("User")

    # For version chaining (self-referential)
    previous_version = relationship("EventVersion", remote_side=[id], backref=backref("next_versions", cascade="all, delete"))

