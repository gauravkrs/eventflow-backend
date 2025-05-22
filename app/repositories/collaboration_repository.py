from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.permission import Permission, RoleEnum
from fastapi import HTTPException, status

class CollaborationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_event_and_user(self, event_id: int, user_id: int) -> Optional[Permission]:
        try:
            return (
                self.db.query(Permission)
                .filter(Permission.event_id == event_id, Permission.user_id == user_id)
                .first()
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch permission")

    def create_role(self, event_id: int, user_id: int, role: RoleEnum) -> Permission:
        try:
            permission = Permission(event_id=event_id, user_id=user_id, role=role)
            self.db.add(permission)
            self.db.flush() 
            return permission
        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create permission")

    def list_by_event(self, event_id: int) -> List[Permission]:
        try:
            return self.db.query(Permission).filter(Permission.event_id == event_id).all()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list permissions")

    def update_role(self, event_id: int, user_id: int, role: RoleEnum) -> Optional[Permission]:
        try:
            share = self.get_by_event_and_user(event_id, user_id)
            if share:
                share.role = role
                self.db.flush()
            return share
        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update permission")

    def delete_permission(self, event_id: int, user_id: int) -> bool:
        try:
            share = self.get_by_event_and_user(event_id, user_id)
            if share:
                self.db.delete(share)
                self.db.flush()
                return True
            return False
        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete permission")
