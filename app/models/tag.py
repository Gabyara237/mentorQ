from datetime import datetime
from sqlmodel import Field, SQLModel


class Tag(SQLModel, table =True):
    __tablename__ = "tags"
    
    id: int | None = Field(default=None, primary_key = True)
    name: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
