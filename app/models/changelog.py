from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Changelog(Base):
    __tablename__ = "changelogs"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)      # fix
    version_id = Column(Integer, nullable=True)                              # fix
    changes = Column(JSON, nullable=True)                                    # fix
    description = Column(String, nullable=True)                              # fix
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)    # fix
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)      # fix

    event = relationship("Event", back_populates="changelogs")

