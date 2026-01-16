from typing import Annotated
from app.models.ticket import TicketStatus
from app.services.ticket_tag_service import TicketTagService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_session
from app.models.user import User, UserRole
from app.schemas.ticket import TicketCreate, TicketResponse
from app.services.ticket_service import TicketService
from app.utils.dependencies import get_current_user


router = APIRouter()

@router.post("/", response_model=TicketResponse,status_code=status.HTTP_201_CREATED)
def create_ticket(session: Annotated[Session,Depends(get_session)], ticket_data: TicketCreate, current_user: Annotated[User, Depends(get_current_user)]):
    ticket = TicketService.create_ticket(session=session, ticket_data=ticket_data, student_id=current_user.id)
    tags = TicketTagService.get_ticket_tags(session,ticket.id)

    return TicketResponse(**ticket.model_dump(), tags=tags)

@router.get("/me", response_model=list[TicketResponse])
def get_user_tickets(session: Annotated[Session,Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)]):
    
    if current_user.role == UserRole.STUDENT:
        tickets = TicketService.get_user_tickets(session=session,student_id = current_user.id)
    else:
        tickets = TicketService.get_mentor_assigned_tickets(session=session,mentor_id=current_user.id)
    
    ticket_ids = [ticket.id for ticket in tickets if ticket.id is not None]
    tags_map = TicketTagService.get_tags_for_tickets(session, ticket_ids)

    return [
        TicketResponse(
            **ticket.model_dump(),
            tags=tags_map.get(ticket.id, [])
        )
        for ticket in tickets
    ]


@router.get('/', response_model=list[TicketResponse] )
def get_open_tickets(session: Annotated[Session, Depends(get_session)], current_user: Annotated[User,Depends(get_current_user)]):
    
    if current_user.role != UserRole.MENTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can view available tickets"
        )
    
    tickets = TicketService.get_open_tickets(session=session)
    ticket_ids = [ticket.id for ticket in tickets if ticket.id is not None]
    tags_map = TicketTagService.get_tags_for_tickets(session, ticket_ids)

    return [
        TicketResponse(
            **ticket.model_dump(),
            tags=tags_map.get(ticket.id, [])
        )
        for ticket in tickets
    ]



@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket_by_id( session: Annotated[Session, Depends(get_session)], ticket_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    ticket = TicketService.get_ticket_by_id(session=session, ticket_id=ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if current_user.role == UserRole.STUDENT:
        if ticket.student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this ticket"
            )

    elif current_user.role == UserRole.MENTOR:
        is_open = ticket.status == TicketStatus.OPEN
        is_assigned_to_me = ticket.assigned_mentor_id == current_user.id

        if not (is_open or is_assigned_to_me):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this ticket"
            )

    tags = TicketTagService.get_ticket_tags(session, ticket.id)
    return TicketResponse(**ticket.model_dump(), tags=tags)



@router.post("/{ticket_id}/accept", response_model=TicketResponse)
def accept_ticket(session: Annotated[Session, Depends(get_session)], ticket_id: int, current_user : Annotated[User, Depends(get_current_user)]):

    if current_user.role != UserRole.MENTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can accept tickets"
        )
    
    ticket = TicketService.accept_ticket(session, ticket_id,current_user.id)

    if not ticket:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    tags = TicketTagService.get_ticket_tags(session, ticket.id)
    return TicketResponse(**ticket.model_dump(), tags=tags)

