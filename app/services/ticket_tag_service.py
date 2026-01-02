
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.tag import Tag
from app.models.ticket import Ticket
from app.models.ticket_tag import TicketTag
from app.services.tag_service import TagService


class TicketTagService:
    @staticmethod
    def add_tag_to_ticket(session: Session, ticket_id: int, tag_name:str) ->TicketTag :
        ticket=session.get(Ticket, ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        tag = TagService.get_or_create_tag(session, tag_name)

        query = select(TicketTag).where((TicketTag.ticket_id== ticket_id) & (TicketTag.tag_id==tag.id))
        ticket_tag= session.exec(query).first()

        if ticket_tag:
            raise HTTPException(status_code=409, detail="Ticket Tag already registered")

        new_ticket_tag=TicketTag(
            ticket_id= ticket_id,
            tag_id=tag.id
        )
        session.add(new_ticket_tag)
        session.commit()
        session.refresh(new_ticket_tag)

        return new_ticket_tag
    
    @staticmethod
    def remove_tag_from_ticket(session: Session,ticket_id:int, tag_id:int) -> None:
        ticket = session.get(Ticket,ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
            
        query= select(TicketTag).where((TicketTag.ticket_id==ticket_id) & (TicketTag.tag_id==tag_id))
        ticket_tag = session.exec(query).first()

        if not ticket_tag:
          raise HTTPException(status_code=404,detail="Ticket Tag not found")
        
        session.delete(ticket_tag)
        session.commit()

        return None

    @staticmethod
    def get_ticket_tags(session: Session, ticket_id: int)-> list[str]:
        ticket = session.get(Ticket, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        statement = (select(Tag.name).join(TicketTag, TicketTag.tag_id==Tag.id).where(TicketTag.ticket_id == ticket_id))
        tag_names = session.exec(statement).all()

        return tag_names
