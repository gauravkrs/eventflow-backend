from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.repositories.collaboration_repository import CollaborationRepository
from app.models.permission import RoleEnum, Permission

class CollaborationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CollaborationRepository(db)

    def share_event(self, event_id: int, user_id: int, role: RoleEnum) -> Permission:
        try:
            if self.repo.get_by_event_and_user(event_id, user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already has access to this event"
                )

            permission = self.repo.create_role(event_id, user_id, role)
            self.db.commit()
            return permission
        except HTTPException:
            raise 
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to share event with user: {str(e)}"
            )

    def list_permission(self, event_id: int) -> List[Permission]:
        try:
            return self.repo.list_by_event(event_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to list permissions: {str(e)}"
            )

    def update_permission(self, event_id: int, user_id: int, role: RoleEnum) -> Permission:
        try:
            share = self.repo.update_role(event_id, user_id, role)
            if not share:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Permission not found for this user and event"
                )
            self.db.commit()
            return share
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update permission: {str(e)}"
            )

    def remove_permission(self, event_id: int, user_id: int):
        try:
            success = self.repo.delete_permission(event_id, user_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Permission not found for this user and event"
                )
            self.db.commit()
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to remove permission: {str(e)}"
            )
