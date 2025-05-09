from uuid import UUID

from sqlalchemy.orm import Session

from src.application.schemas.invitation import (
    InvitationCreate,
    InvitationSchema,
)
from src.infrastructure.postgres.models.invitations import Invitation


class InvitationNotFoundError(Exception):
    """Исключение, вызываемое, если приглашение не найдено"""

    def __str__(self):
        return "Приглашение не найдено"


class InvitationsRepository:
    def get_invitation(self, session: Session, token: UUID) -> InvitationSchema:
        invitation = session.query(Invitation).filter_by(token=token).first()
        if not invitation:
            raise InvitationNotFoundError
        return InvitationSchema.model_validate(invitation)

    def create_invitation(self, session: Session, invitation_data: InvitationCreate) -> InvitationSchema:
        new_invitation = Invitation(**invitation_data.model_dump(), is_accepted=False)
        session.add(new_invitation)
        session.commit()
        session.refresh(new_invitation)

        return InvitationSchema.model_validate(new_invitation)

    def accept_invitation(self, session: Session, token: UUID) -> InvitationSchema:
        invitation = session.query(Invitation).filter_by(token=token).first()
        if not invitation:
            raise InvitationNotFoundError
        invitation.is_accepted = True
        session.commit()
        session.refresh(invitation)
        return InvitationSchema.model_validate(invitation)


invitations_repository = InvitationsRepository()
