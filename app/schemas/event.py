from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_recurring: Optional[bool] = False
    reccurrence_pattern: Optional[str] =None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    location: Optional[str]
    is_recurring: Optional[bool]
    reccurrence_pattern: Optional[str]

class EventOut(EventBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
