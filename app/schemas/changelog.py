from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class ChangeDetail(BaseModel):
    old: Any
    new: Any

class ChangelogOut(BaseModel):
    id: int
    event_id: int
    version_id: int
    changes: Dict[str, ChangeDetail]
    description: str
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True

        