
from sqlmodel import Session, select
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate
from app.services.ticket_tag_service import TicketTagService



class TicketService:
    @staticmethod
    def create_ticket(session: Session, ticket_data:TicketCreate, student_id: int)-> Ticket:
        
        new_ticket = Ticket(
            title = ticket_data.title,
            description= ticket_data.description,
            student_id= student_id
        )
        session.add(new_ticket)
        session.commit()
        session.refresh(new_ticket)
        
        for tag_name in ticket_data.tags:
            try:
                TicketTagService.add_tag_to_ticket(session,  new_ticket.id,tag_name)
            except:
                pass
                    
        return new_ticket

    @staticmethod
    def get_user_tickets(session: Session,student_id: int)-> list[Ticket]:
        query = select(Ticket).where(Ticket.student_id==student_id)
        tickets = session.exec(query).all()

        return tickets
    
    @staticmethod
    def get_ticket_by_id(session: Session,ticket_id: int)->Ticket |None:
        return session.get(Ticket,ticket_id)
    
    @staticmethod
    def get_open_tickets(session: Session, mentor_id: int)-> list[Ticket]:
        query = select(Ticket).where(Ticket.status =="open").order_by(Ticket.created_at.desc())
        tickets = session.exec(query).all()

        return tickets
    
    @staticmethod
    def get_mentor_assigned_tickets(session:Session, mentor_id: int) -> list[Ticket]:
        query = select(Ticket).where(Ticket.assigned_at==mentor_id).order_by(Ticket.created_at.desc())
        Tickets = session.exec(query).all()