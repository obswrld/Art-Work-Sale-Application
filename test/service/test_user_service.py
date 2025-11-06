import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "test/service/Art-Work-Sale-Application")))
from unittest.mock import patch, MagicMock
from passlib.hash import bcrypt
from schemas.user_schema import CreateUserSchema
from services.user_service import UserService

import pytest


@pytest.fixture
def mock_user_repo():
    with patch('services.user_service.UserRepository') as mock:
        yield mock

@pytest.fixture
def user_service(mock_user_repo):
    return UserService()

@pytest.fixture
def sample_user():
    return MagicMock(
        id=1,
        first_name="John",
        last_name="Smith",
        email="johnsmith1@gmail.com",
        role="BUYER",
        is_verified=True,
        passwword=bcrypt.hash("LamineYamal10!")
    )

def test_register_user(mock_user_repo, user_service):
    mock_user_repo().find_by_email.return_value = None
    mock_user_repo().create_user.return_value = MagicMock(
        id=1,
        first_name="John",
        last_name="Smith",
        email="johnsmith1@gmail.com",
        role="BUYER",
        is_verified=False,
    )
    user_data = CreateUserSchema(
        first_name="John",
        last_name="Smith",
        email="johnsmith1@gmail.com",
        password="LamineYamal10!",
        confirm_password="LamineYamal10!"
    )
    result = user_service.register(user_data)
    assert result.email == "johnsmith1@gmail.com"
    assert result.is_verified is False
    mock_user_repo().create_user.assert_called_once()