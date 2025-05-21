from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.permission import Permission, RoleEnum

class CollaborationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_event_and_user(self, event_id: int, user_id: int) -> Optional[Permission]:
        return (
            self.db.query(Permission)
            .filter(Permission.event_id == event_id, Permission.user_id == user_id)
            .first()
        )

    def create_role(self, event_id: int, user_id: int, role: RoleEnum) ->  Permission:
        permission = Permission(event_id= event_id, user_id = user_id, role = role)
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission
    
    def list_by_event(self, event_id: int) -> List[Permission]:
        return self.db.query(Permission).filter(Permission.event_id == event_id)
    
    def update_role(self, event_id: int, user_id: int, role: RoleEnum) -> Optional[Permission]:
        share = self.get_by_event_and_user(event_id, user_id)
        if share:
            share.role = role
            self.db.commit()
            self.db.refresh(share)
        return share
    
    def delete_permission(self, event_id: int, user_id: int) -> bool:
        share = self.get_by_event_and_user(event_id, user_id)
        if share:
            self.db.delete(share)
            self.db.commit()
            return True
        return False
    

