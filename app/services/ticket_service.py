
from sqlmodel import Session, select
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate



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
        
        return new_ticket

    @staticmethod
    def get_user_tickets(session: Session,student_id: int)-> list[Ticket]:
        query = select(Ticket).where(Ticket.student_id==student_id)
        tickets = session.exec(query).all()

        return tickets
    
    @staticmethod
    def get_ticket_by_id(session: Session,ticket_id: int)->Ticket |None:
        return session.get(Ticket,ticket_id)