from pydantic import BaseModel
from typing import Any
from datetime import datetime

class EventVersionOut(BaseModel):
    id: int
    event_id: int
    version_data: dict[str, Any]
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True
