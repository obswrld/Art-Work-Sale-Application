import sys
import os
from pydantic import ValidationError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "test/service/Art-Work-Sale-Application")))
from unittest.mock import patch, MagicMock
from passlib.hash import bcrypt
from schemas.user_schema import CreateUserSchema, LoginUserSchema
from services.user_service import UserService
from exceptions.exception import (
    InvalidPasswordCredentials,
    UserNotFound,
    UserAlreadyExists,
    CredentialsMissMatchError,
    MissingRequiredField
)
import pytest

@pytest.fixture
def mock_user_repo(mocker):
    mock = mocker.patch("services.user_service.UserRepository")
    return mock

@pytest.fixture
def user_service(mock_user_repo):
    service = UserService()
    service.repo = mock_user_repo()
    return service

@pytest.fixture
def sample_user():
    user = MagicMock()
    user.id=1
    user.first_name="John"
    user.last_name="Smith"
    user.email="johnsmith1@gmail.com"
    user.password=bcrypt.hash("LamineYamal10!")
    user.role="BUYER"
    user.is_verified=True
    user.verification_token=None
    return user

def test_register_user(mock_user_repo, user_service):
    mock_user_repo().find_by_email.return_value = None
    mock_user_repo().create_user.return_value = MagicMock(
        id=1,
        first_name="John",
        last_name="Smith",
        email="johnsmith1@gmail.com",
        role="BUYER",
        password="hashed",
        verification_token="toke1234",
    )
    user_data = CreateUserSchema(
        first_name="John",
        last_name="Smith",
        email="johnsmith1@gmail.com",
        password="LamineYamal10!",
        confirm_password="LamineYamal10!",
    )
    result = user_service.register(user_data)
    assert result.email == "johnsmith1@gmail.com"
    mock_user_repo().create_user.assert_called_once()

def test_register_invalid_email_credentials(user_service):
    with pytest.raises(ValidationError):
        CreateUserSchema(
            first_name="James",
            last_name="Glory",
            email="JamesGlory",
            password="password123",
            confirm_password="password123",
        )

def test_register_invalid_or_weak_password_credentials(user_service):
    with pytest.raises(ValidationError):
        data = CreateUserSchema(
            first_name="James",
            last_name="Glory",
            email="jamesglory12@gmail.com",
            password="passW",
            confirm_password="passW"
        )

# def test_register_existing_email(mock_user_repo, user_service):
#     mock_user_repo().find_by_email.return_value = sample_user
#     user_data = CreateUserSchema(
#         first_name="John",
#         last_name="Smith",
#         email="johnsmith1@gmail.com",
#         password="LamineYamal10!",
#         confirm_password="LamineYamal10!"
#     )
#     with pytest.raises(UserAlreadyExists):
#         user_service.register(user_data)
#
# def test_login_success(mock_user_repo, user_service, sample_user):
#     mock_user_repo().find_by_email.return_value = sample_user
#     user_data = LoginUserSchema(
#         email="johnsmith1@gmail.com",
#         password="LamineYamal10!",
#     )
#     result = user_service.login_user(user_data)
#     assert result.email == "johnsmith1@gmail.com"
#     assert result.is_verified is True
#
# def test_unverified_user(mock_user_repo, user_service, sample_user):
#     sample_user.is_verified = False
#     mock_user_repo().find_by_email.return_value = sample_user
#
#     login_data = LoginUserSchema(
#         email="johnsmith1@gmail.com",
#         password="LamineYamal10!",
#     )
#     with pytest.raises(ValueError):
#         user_service.login_user(login_data)
#
# def test_login_invalid_credentials(mock_user_repo, user_service):
#     mock_user_repo().find_by_email.return_value = None
#     login_data = LoginUserSchema(
#         email="johnsmith11@gmail.com",
#         password="LamineYamal11!",
#     )
#     with pytest.raises(ValueError):
#         user_service.login_user(login_data)
#
# def test_verify_user_success(mock_user_repo, user_service, sample_user):
#     mock_user_repo().find_by_verification_code.return_value = sample_user
#
#     result = user_service.verify_user("Token234")
#     assert result is True
#     mock_user_repo().save.assert_called_once()
#
# def test_verify_invalid_token(mock_user_repo, user_service):
#     mock_user_repo().find_by_verification_code.return_value = None
#
#     with pytest.raises(ValueError):
#         user_service.verify_user("Token333")