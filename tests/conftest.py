
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.models.user import UserRole
from app.schemas.user import UserCreate
from app.services.auth_service import AuthService
from app.schemas.ticket import TicketCreate
from app.services.ticket_service import TicketService


@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh database session for each test"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def test_student(session: Session):
    """Create a test student user"""
    user_data = UserCreate(
        username="teststudent",
        email="student@test.com",
        password="testpass123",
        role=UserRole.STUDENT,
    )
    return AuthService.create_user(session, user_data)


@pytest.fixture
def test_mentor(session: Session):
    """Create a test mentor user"""
    user_data = UserCreate(
        username="testmentor",
        email="mentor@test.com",
        password="testpass123",
        role=UserRole.MENTOR,
    )
    return AuthService.create_user(session, user_data)



@pytest.fixture
def open_ticket(session, test_student):
    data = TicketCreate(
        title="Need help with FastAPI",
        description="Dependency injection confusion",
        tags=[]
    )
    return TicketService.create_ticket(session, data, student_id=test_student.id)

@pytest.fixture
def second_open_ticket(session, test_student):
    data = TicketCreate(
        title="SQLModel relationships",
        description="Many-to-many setup",
        tags=[]
    )
    return TicketService.create_ticket(session, data, student_id=test_student.id)
