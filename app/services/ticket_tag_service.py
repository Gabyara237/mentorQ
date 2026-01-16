
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
    def get_ticket_tags(session: Session, ticket_id: int) -> list[str]:
        statement = (
            select(Tag.name)
            .join(TicketTag, TicketTag.tag_id == Tag.id)
            .where(TicketTag.ticket_id == ticket_id)
        )
        return session.exec(statement).all()


    @staticmethod
    def get_tags_for_tickets(session: Session, ticket_ids: list[int]) -> dict[int, list[str]]:
       
        if not ticket_ids:
            return {}

        statement = (
            select(TicketTag.ticket_id, Tag.name)
            .join(Tag, Tag.id == TicketTag.tag_id)
            .where(TicketTag.ticket_id.in_(ticket_ids))
        )

        rows = session.exec(statement).all()

        tags_map: dict[int, list[str]] = {tid: [] for tid in ticket_ids}
        for ticket_id, tag_name in rows:
            tags_map[ticket_id].append(tag_name)

        return tags_map
