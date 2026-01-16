
from enum import Enum
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class TicketStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Ticket(SQLModel, table= True):
    __tablename__= "tickets"

    id: int | None = Field(default = None, primary_key = True )
    title: str 
    description: str
    status: TicketStatus = Field(default=TicketStatus.OPEN, index=True)
    student_id: int = Field(foreign_key="users.id", index=True)
    assigned_mentor_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    solution: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    assigned_at: datetime | None = Field(default=None)
    resolved_at: datetime | None = Field(default=None)
    closed_at: datetime | None = Field(default=None)

