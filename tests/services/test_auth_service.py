import pytest
from fastapi import HTTPException

from app.schemas.user import UserCreate
from app.services.auth_service import AuthService
from app.models.user import UserRole


def test_create_user_success_normalizes_and_hashes(session):
    user_data = UserCreate(
        username="  NewUser  ",
        email=" NewUser@Test.com ",
        password="password123",
        role=UserRole.STUDENT,
    )

    user = AuthService.create_user(session, user_data)

    assert user.id is not None
    assert user.username == "newuser"               
    assert user.email == "newuser@test.com"         
    assert user.role == UserRole.STUDENT
    assert user.password_hash is not None
    assert user.password_hash != "password123"      

@pytest.mark.parametrize(
    "username,email,expected_detail",
    [
        ("teststudent", "different@test.com", "Username already registered"),
        (" TESTSTUDENT   ", "another@test.com", "Username already registered"),  
        ("anotheruser", "student@test.com", "Email already registered"),
        ("anotheruser", "  STUDENT@TEST.COM ", "Email already registered"),     
    ],
)

def test_create_user_duplicates_raise_409(session, test_student, username, email, expected_detail):
    user_data = UserCreate(
        username=username,
        email=email,
        password="password123",
        role=UserRole.STUDENT,
    )

    with pytest.raises(HTTPException) as exc_info:
        AuthService.create_user(session, user_data)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == expected_detail


def test_authenticate_user_success_accepts_normalized_username(session):
    user_data = UserCreate(
        username="authuser",
        email="auth@test.com",
        password="correctpassword",
        role=UserRole.STUDENT,
    )
    AuthService.create_user(session, user_data)

    authenticated = AuthService.authenticate_user(session, "  AUTHUSER  ", "correctpassword")

    assert authenticated is not None
    assert authenticated.username == "authuser"


@pytest.mark.parametrize(
    "username,password",
    [
        ("authuser2", "wrongpassword"),
        ("nonexistent", "anypassword"),
    ],
)
def test_authenticate_user_returns_none_on_failure(session, username, password):
    if username == "authuser2":
        user_data = UserCreate(
            username="authuser2",
            email="auth2@test.com",
            password="correctpassword",
            role=UserRole.STUDENT,
        )
        AuthService.create_user(session, user_data)

    authenticated = AuthService.authenticate_user(session, username, password)
    assert authenticated is None
