from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Changelog(Base):
    __tablename__ = "changelogs"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    version_id = Column(Integer)  # FK optional if soft linking
    changes = Column(JSON)  # {"field": {"old": ..., "new": ...}}
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))

    event = relationship("Event", back_populates="changelogs")
