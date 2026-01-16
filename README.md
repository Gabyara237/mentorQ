# MentorQ

![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![SQLite](https://img.shields.io/badge/database-SQLite-blue?logo=sqlite)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

**MentorQ** is a REST API mentorship platform connecting programming students with volunteer mentors through an intelligent ticket-based system with technology tag matching.

> **Project Status:** Currently in active development. Core MVP features are being implemented. 

## Description

MentorQ addresses a critical gap in programming education: **access to personalized technical mentorship**. Self-taught developers and bootcamp students often struggle to get timely help with specific technical challenges.

MentorQ creates a structured mentorship ecosystem where:

- **Students** create tickets describing technical problems with relevant technology tags
- **Mentors** browse tickets filtered by their areas of expertise
- **Intelligent matching** happens through tag-based filtering (e.g., mentor with `["python", "fastapi"]` sees tickets with those tags)
- **Knowledge base** grows as resolved tickets become searchable resources
- **Real-time sessions** (upcoming) enable live coding assistance via WebSocket


## Current Features

### Authentication & Authorization
- [x] JWT-based authentication with bcrypt password hashing
- [x] Role-based access control (Student vs Mentor)
- [x] Secure session management
- [x] `/auth/signup`, `/auth/signin`, `/auth/me` endpoints

### Ticket System

**Students can:**
- [x] Create tickets with title, description, and technology tags
- [x] View all their tickets (any status)
- [x] View specific ticket details with tags
- [ ] Close resolved tickets *(in progress)*
- [ ] Delete Open tickets
- [ ] Browse all resolved tickets (knowledge base)
- [ ] Filter resolved tickets by technology
- [ ] Search resolved tickets by keyword

**Mentors can:**
- [x] Browse all Open tickets
- [x] View tickets filtered by role (mentors see Open, students see their own)
- [x] Accept tickets (status: `Open` → `Assigned`)
- [ ] Post solutions to assigned tickets *(in progress)*
- [ ] View all tickets they've resolved

### Tag System
- [x] Technology tags for precise matching (e.g., "python", "react", "fastapi")
- [x] Many-to-many relationships via junction tables (`TicketTag`)
- [x] Mentor ↔ Tag relationship defined via `MentorTag` junction table (model implemented)
- [x] Automatic tag normalization (prevents "Python" vs "python" duplicates)
- [x] Tags included in ticket creation and retrieval
- [ ] Mentor expertise management (add/remove/list mentor tags)
- [ ] Tag-based mentor-ticket matching


### Technical Highlights
- **Layered architecture**: Separation of concerns (models, schemas, services, routers, utils)
- **Query optimization**: Refactored N+1 queries to batch JOIN-based queries, significantly reducing query overhead and improving scalability
- **Data normalization**: Automatic `.strip().lower()` on all user inputs
- **Consistent error handling**: HTTP status codes (401, 403, 404, 409)
- **API documentation**: Auto-generated interactive docs with Swagger UI
- **Security**: Password hashing, JWT tokens, role-based authorization


## Planned Features

### Phase 1: Complete Core MVP 
- [ ] Mentor posts solution (status: `Assigned` → `Resolved`)
- [ ] Student closes ticket (status: `Resolved` → `Closed`)
- [ ] Student deletes Open tickets
- [ ] Reviews system (students rate mentors after closure)
- [ ] Student views mentor profile
- [ ] Mentor adds expertise tags to profile

### Phase 2: Knowledge Base 
- [ ] Browse all resolved tickets (public knowledge base)
- [ ] Filter resolved tickets by technology tags
- [ ] Search resolved tickets by keyword
- [ ] Upvote helpful resolved tickets
- [ ] Bookmark resolved tickets for later

### Phase 3: Notifications 
- [ ] Student receives notification when mentor accepts ticket
- [ ] Mentor receives notification when ticket matching their tags is posted
- [ ] Notification history page
- [ ] Mark notifications as read

### Phase 4: Real-Time Sessions 
- [ ] **WebSocket integration** for real-time communication
- [ ] Session scheduling system
- [ ] Request 15-min chat with mentor
- [ ] Accept/decline chat requests

### Phase 5: Advanced Features *(Future)*
- [ ] Mentor availability toggle (available/busy)
- [ ] Mentor stats dashboard (tickets resolved, avg response time)
- [ ] Student dashboard with activity summary
- [ ] Edit profile (bio, avatar, skills)
- [ ] Mentor leaderboards and achievements
- [ ] Follow mentors to see their activity
- [ ] Student progress tracking


## Tech Stack

### Backend Framework
- **FastAPI** - Modern, high-performance web framework with automatic API documentation
- **Pydantic** - Data validation and serialization with Python type hints
- **Uvicorn** - Lightning-fast ASGI server

### Database & ORM
- **SQLite** (development) - Lightweight, file-based database for rapid iteration
- **PostgreSQL** (planned for production) - Scalable, production-ready relational database
- **SQLAlchemy + SQLModel** - Powerful ORM with Pydantic integration

### Authentication & Security
- **JWT (JSON Web Tokens)** - Stateless authentication
- **bcrypt** - Secure password hashing with salt
- **python-jose** - JWT encoding/decoding

### Testing
- **pytest** – Unit testing framework for service-layer testing
- **FastAPI TestClient** *(planned)* – Integration testing for API endpoints
- **SQLite (in-memory)** – Isolated and fast test database

### Planned Integrations
- **WebSocket** - Real-time bidirectional communication for live sessions
- **Redis** - Session caching and pub/sub for notifications
- **SendGrid/Mailgun** - Email notifications


## Architecture

MentorQ follows a **layered architecture** ensuring separation of concerns, testability, and scalability:
```
mentorQ/
├── app/
│   ├── models/                 # SQLModel database tables
│   │   ├── __init__.py
│   │   ├── user.py             # User (Student/Mentor roles)
│   │   ├── ticket.py           # Ticket with status state machine
│   │   ├── tag.py              # Technology tags (unique, normalized)
│   │   ├── ticket_tag.py       # Junction: Ticket ↔ Tag (many-to-many)
│   │   ├── mentor_tag.py       # Junction: Mentor ↔ Tag (many-to-many, model implemented, service/endpoints planned)
│   │   ├── review.py           # (planned) Student reviews for mentors
│   │   └── notification.py     # (planned) User notifications
│   │
│   ├── schemas/                # Pydantic models for validation
│   │   ├── __init__.py
│   │   ├── user.py             # UserCreate, UserLogin, UserResponse, Token
│   │   ├── ticket.py           # TicketCreate, TicketResponse (with tags)
│   │   └── tag.py              # TagCreate, TagResponse
│   │
│   ├── services/               # Business logic layer (HTTP-coupled for MVP, domain exceptions planned)
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── ticket_service.py
│   │   ├── tag_service.py
│   │   └── ticket_tag_service.py
│   │
│   ├── routers/                # API endpoints (HTTP layer)
│   │   ├── __init__.py
│   │   ├── auth.py             # /auth/signup, /auth/signin, /auth/me
│   │   └── tickets.py          # /tickets/* (CRUD + mentor actions)
│   │
│   ├── utils/                  # Reusable utilities
│   │   ├── __init__.py
│   │   ├── security.py         # Password hashing, JWT creation/validation
│   │   └── dependencies.py     # FastAPI dependencies (get_current_user, etc.)
│   │
│   ├── database.py             # Database connection and session management
│   └── main.py                 # FastAPI app initialization and configuration
│
├── tests/                      # Automated tests
│   ├── services/               # Unit tests for service layer
│   │    ├── test_auth_service.py
│   │    └── test_ticket_service.py
│   └── integration/            # (planned) API integration tests
│
├── .env                        # Environment variables (SECRET_KEY, DATABASE_URL)
├── .gitignore
├── requirements.txt
└── README.md
```


## Database Design

### Entity Relationship Diagram

![MentorQ ERD](https://trello.com/1/cards/69539aa0094ab7d14fc96e70/attachments/6968ad88ed85a3be26ce546c/download/ERD.png)

*Complete ERD showing relationships between User, Ticket, Tag, Review, Notification, and junction tables*

### Key Relationships

**User ↔ Ticket:**
- **One-to-Many**: Student creates many tickets (`Ticket.student_id → User.id`)
- **One-to-Many**: Mentor accepts many tickets (`Ticket.assigned_mentor_id → User.id`)

**Ticket ↔ Tag:**
- **Many-to-Many** via `TicketTag` junction table
- A ticket can have multiple tags (`["python", "fastapi", "async"]`)
- A tag can be on multiple tickets

**User (Mentor) ↔ Tag:**
- **Many-to-Many** via `MentorTag` junction table
- A mentor has expertise in multiple tags
- A tag can be expertise of multiple mentors

**User ↔ Review:**
- **One-to-Many**: Student writes many reviews
- **One-to-Many**: Mentor receives many reviews


## Testing Strategy

### Current Approach
- Manual validation via Swagger UI for complete request/response flows (authentication, permissions, ticket lifecycle)
- Automated **unit tests** for the service layer using **pytest** with an in-memory SQLite database

### Implemented Testing (Service Layer)

```bash
# Run all tests
pytest

# Run only service-layer unit tests
pytest tests/services

# Run specific service tests
pytest tests/services/test_auth_service.py
pytest tests/services/test_ticket_service.py
```

### What Is Covered (Unit Tests)

#### AuthService
- User creation with normalization (username/email)
- Password hashing verification
- Duplicate username/email → `409 Conflict`
- Authentication success and failure cases

#### TicketService
- Ticket creation (default status = `OPEN`)
- Fetching tickets by student
- Fetching open tickets ordered by creation date
- Accept ticket flow:
  - Ticket not found → `404 Not Found`
  - Ticket not open → `409 Conflict`
  - Successful assignment to mentor

### Planned Testing (Next)

**Integration Tests (API Endpoints):**
```bash
# Test complete request/response flow
pytest tests/integration/test_auth_endpoints.py
pytest tests/integration/test_ticket_endpoints.py
```

**Coverage Report:**
```bash
pytest --cov=app --cov-report=html
# Target: >80% coverage
```


## Getting Started

### Prerequisites
- **Python 3.11+**
- **pip** (Python package manager)
- **Git**

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/gabyara237/mentorQ.git
cd mentorQ
```

**2. Create virtual environment:**
```bash
python -m venv .venv

# Activate:
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt --break-system-packages
```

**4. Configure environment variables:**

Create a `.env` file in the project root:
```bash
# Database
DATABASE_URL=sqlite:///./mentorq.db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**5. Run the application:**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

**6. Access interactive API documentation:**
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`


## Future Roadmap

### Technical Enhancements

**Database:**
- Migrate to PostgreSQL for production
- Implement database migrations (Alembic)
- Add full-text search for tickets (PostgreSQL FTS)

**Testing:**
- Expand unit test coverage across services
- Add API integration tests
- Maintain test coverage > 80%

**Architecture:**
- Refactor to custom domain exceptions
- Implement repository pattern for data access
- Add Redis caching for frequently accessed data


## Project Management

### Resources
- **Planning Board**: [Trello - MentorQ](https://trello.com/b/03gCXeA9/mentorq)
- **Database Design**: [ERD Image](https://trello.com/1/cards/69539aa0094ab7d14fc96e70/attachments/6968ad88ed85a3be26ce546c/download/ERD.png)
- **Repository**: [GitHub - gabyara237/mentorQ](https://github.com/gabyara237/mentorQ)


## Project Status

**Last Updated:** January 15, 2026

**Current Focus:** Completing core MVP (mentor solution posting + student ticket closure + reviews system)

**Next Milestone:** WebSocket integration for real-time mentoring sessions

**Deployment:** Planned (Render / Railway / Fly.io)

---


Questions? Feel free to open an issue or reach out directly.