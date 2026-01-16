import pytest
from fastapi import HTTPException

from app.models.ticket import TicketStatus
from app.schemas.ticket import TicketCreate
from app.services.ticket_service import TicketService


def test_create_ticket_success_defaults_to_open(session, test_student):
    data = TicketCreate(
        title="Help with JWT",
        description="Token validation issue",
        tags=[]
    )

    ticket = TicketService.create_ticket(session, data, student_id=test_student.id)

    assert ticket.id is not None
    assert ticket.title == "Help with JWT"
    assert ticket.description == "Token validation issue"
    assert ticket.student_id == test_student.id
    assert ticket.status == TicketStatus.OPEN
    assert ticket.created_at is not None



def test_get_user_tickets_returns_only_student_tickets(session, test_student, test_mentor):

    ticket1 = TicketService.create_ticket(session, TicketCreate(title="A", description="A", tags=[]), test_student.id)
    ticket2 = TicketService.create_ticket(session, TicketCreate(title="B", description="B", tags=[]), test_student.id)

    other = TicketService.create_ticket(session, TicketCreate(title="C", description="C", tags=[]), test_mentor.id)

    tickets = TicketService.get_user_tickets(session, student_id=test_student.id)

    ids = {ticket.id for ticket in tickets}
    assert ticket1.id in ids
    assert ticket2.id in ids
    assert other.id not in ids


def test_accept_ticket_returns_none_when_not_found(session):
    result = TicketService.accept_ticket(session, ticket_id=99999, mentor_id=1)
    assert result is None


def test_accept_ticket_raises_409_when_not_open(session, test_student):
    ticket = TicketService.create_ticket(session, TicketCreate(title="X", description="X", tags=[]), test_student.id)
    ticket.status = TicketStatus.ASSIGNED
    session.add(ticket)
    session.commit()

    with pytest.raises(HTTPException) as exc_info:
        TicketService.accept_ticket(session, ticket_id=ticket.id, mentor_id=5)

    assert exc_info.value.status_code == 409
    assert "not available for acceptance" in exc_info.value.detail.lower()


def test_accept_ticket_success_assigns_ticket(session, test_student):
    ticket = TicketService.create_ticket(session, TicketCreate(title="X", description="X", tags=[]), test_student.id)

    updated = TicketService.accept_ticket(session, ticket_id=ticket.id, mentor_id=42)

    assert updated is not None
    assert updated.status == TicketStatus.ASSIGNED
    assert updated.assigned_mentor_id == 42
    assert updated.assigned_at is not None
