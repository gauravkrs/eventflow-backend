from pydantic import BaseModel
from typing import Any, List, Dict
from datetime import datetime

class EventVersionOut(BaseModel):
    id: int
    event_id: int
    version_number: int
    version_data: dict[str, Any]
    created_at: datetime
    created_by: int
    previous_version_id: int | None

    class Config:
        from_attributes = True

class ChangelogOut(BaseModel):
    versions: List[EventVersionOut]

class DiffOut(BaseModel):
    differences: Dict[str, Dict[str, Any]]