
from datetime import datetime
from pydantic import BaseModel

from app.models.ticket import TicketStatus


class TicketCreate(BaseModel):
    title: str
    description: str
    tags: list[str] = []

class TicketResponse(BaseModel):
    id: int
    title: str
    description:str
    tags:list[str]= []
    status: TicketStatus
    student_id:int
    assigned_mentor_id: int | None
    solution: str | None
    created_at: datetime 
    assigned_at: datetime | None  
    resolved_at: datetime | None  
    closed_at: datetime | None   

    