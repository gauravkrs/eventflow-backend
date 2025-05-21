from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.repositories.collaboration_repository import CollaborationRepository
from app.models.permission import RoleEnum, Permission

class CollaborationService:
    def __init__(self, db: Session):
        self.repo = CollaborationRepository(db)

    def share_event(self, event_id: int, user_id: int, role: RoleEnum) -> Permission:
        if self.repo.get_by_event_and_user(event_id, user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already has access")
        return self.repo.create_role(event_id, user_id, role)
    
    def list_permission(self, event_id: int) -> List[Permission]:
        return self.repo.list_by_event(event_id)
    
    def update_permission(self, event_id: int, user_id: int, role: RoleEnum) -> Permission:
        share = self.repo.update_role(event_id, user_id, role)
        if not share:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return share
    
    def remove_permission(self, event_id: int, user_id: int):
        try:
            success = self.repo.delete_permission(event_id, user_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Permission not found"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove permission"
            )