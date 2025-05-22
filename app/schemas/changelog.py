from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class ChangelogOut(BaseModel):
    id: int
    event_id: int
    version_id: Optional[int]
    changes: Optional[Dict[str, Dict[str, str]]]
    description: Optional[str]
    created_at: datetime
    created_by: Optional[int]

    class Config:
        from_attributes = True
