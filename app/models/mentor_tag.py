
from datetime import datetime
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class MentorTag(SQLModel, table =True ):
    __tablename__ = "mentor_tags"
    __table_args__ = (UniqueConstraint("mentor_id", "tag_id"),)

    id: int | None = Field(default=None, primary_key= True )
    mentor_id: int = Field(foreign_key="users.id", index=True)
    tag_id : int  = Field(foreign_key="tags.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
