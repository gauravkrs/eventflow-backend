from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.event import EventBase, EventUpdate, EventOut, EventCreateBatch
from app.services.event_service import EventService
from app.schemas.user import UserOut
from app.db.base import get_db
from app.core.deps import get_current_user
from typing import List

router = APIRouter(prefix="/api/events", tags=["Events"])

@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
async def create_event(
    payload: EventBase,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    print(payload)
    try:
        service = EventService(db)
        event = service.create_event(user.id, payload)
        return event
    except Exception as e:
        # Optional: log error e here
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event"
        )
@router.get("/", response_model=List[EventOut])
async def list_events(db: Session = Depends(get_db), user= Depends(get_current_user)):
    try:
        service = EventService(db)
        return service.list_events(user.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list events")
    
@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    service =  EventService(db)
    return service.get_event(event_id)

@router.put("/{event_id}", response_model=EventOut)
async def update_event(event_id: int, payload: EventUpdate, db: Session = Depends(get_db)):
    try:
        service = EventService(db)
        return service.update_event(event_id, payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update events") 

@router.post("/batch", response_model=List[EventOut], status_code=status.HTTP_201_CREATED)
async def create_batch_events( data: EventCreateBatch,db: Session = Depends(get_db),
current_user: UserOut = Depends(get_current_user)):
    try:
        service = EventService(db)
        return service.create_batch(data, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create batch") 
    

@router.delete("/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    try:
        service = EventService(db)
        return service.delete_event(event_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete events") 