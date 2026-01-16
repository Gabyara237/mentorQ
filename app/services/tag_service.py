
from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.tag import Tag


class TagService:

    @staticmethod
    def create_tag(session: Session, name: str)-> Tag:
        
        normalized_name = name.strip().lower()
        query = select(Tag).where(Tag.name == normalized_name)
        tag = session.exec(query).first()

        if tag:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Tag already registered")
        
        new_tag = Tag(
            name= normalized_name
        )

        session.add(new_tag)
        session.commit()
        session.refresh(new_tag)

        return new_tag
    
    @staticmethod
    def get_all_tags(session: Session)->list[Tag]:
        query = select(Tag)
        tags = session.exec(query).all()
        return tags
    
    @staticmethod
    def get_or_create_tag(session:Session, name: str)-> Tag:
        normalized_name = name.strip().lower()
        query= select(Tag).where(Tag.name== normalized_name)
        tag = session.exec(query).first()

        if not tag:
          tag=  TagService.create_tag(session,name)
        
        return tag
