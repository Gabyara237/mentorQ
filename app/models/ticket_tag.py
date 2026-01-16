
from datetime import datetime
from time import timezone
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel



class TicketTag(SQLModel, table= True):
    __tablename__ ="ticket_tags"
    __table_args__ = (UniqueConstraint("ticket_id", "tag_id"),)
    
    id: int | None = Field(default= None, primary_key=True)
    ticket_id: int = Field(foreign_key="tickets.id")
    tag_id: int = Field(foreign_key="tags.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
