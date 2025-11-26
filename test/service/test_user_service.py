import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "test/service/Art-Work-Sale-Application")))
import pytest
from unittest.mock import MagicMock, patch
from passlib.hash import bcrypt
from datetime import datetime
from pydantic import ValidationError
from repositories.user_repo import UserRepository
from schemas.user_schema import CreateUserSchema, LoginUserSchema, UserResponseSchema
from services.user_service import UserService


@pytest.fixture
def mock_user_repo(mocker):
    mock_repo = MagicMock(spec=UserRepository)
    mocker.patch("services.user_service.UserRepository", return_value=mock_repo)
    return mock_repo


@pytest.fixture
def user_service(mock_user_repo):
    service = UserService()
    service.repo = mock_user_repo
    return service


@pytest.fixture
def sample_user():
    user = MagicMock()
    user.id = 1
    user.first_name = "John"
    user.last_name = "Smith"
    user.email = "johnsmith1@gmail.com"
    user.password = bcrypt.hash("LamineYamal10!")
    user.role = "BUYER"
    user.is_verified = True
    user.verification_code = None
    user.created_at = datetime.now()
    return user


@pytest.fixture
def unverified_user():
    user = MagicMock()
    user.id = 2
    user.first_name = "Gabriel"
    user.last_name = "Samson"
    user.email = "gabisam123@gmail.com"
    user.password = bcrypt.hash("Lewyword10!")
    user.role = "BUYER"
    user.is_verified = False
    user.verification_code = "token_abc123"
    user.created_at = datetime.now()
    return user


def test_register_user_success(mock_user_repo, user_service, sample_user):
    mock_user_repo.find_by_email.return_value = None
    mock_user_repo.create_user.return_value = sample_user
    user_data = CreateUserSchema(
        first_name="John",
        last_name="Smith",
        email="johnsmith1@gmail.com",
        password="LamineYamal10!",
        confirm_password="LamineYamal10!",
    )
    result = user_service.register(user_data)
    assert result.email == "johnsmith1@gmail.com"
    assert result.first_name == "John"
    assert result.last_name == "Smith"
    mock_user_repo.find_by_email.assert_called_once_with("johnsmith1@gmail.com")
    mock_user_repo.create_user.assert_called_once()


def test_register_invalid_email_format(user_service):
    with pytest.raises(ValidationError):
        CreateUserSchema(
            first_name="James",
            last_name="Glory",
            email="JamesGlory",
            password="ValidPass123!",
            confirm_password="ValidPass123!",
        )


def test_register_weak_password_too_short(user_service):
    with pytest.raises(ValidationError) as exc_info:
        CreateUserSchema(
            first_name="James",
            last_name="Glory",
            email="jamesglory1@gmail.com",
            password="Pass1!",
            confirm_password="Pass1!",
        )
    assert "at least 8 characters" in str(exc_info.value).lower()


def test_register_weak_password_no_uppercase(mock_user_repo, user_service):
        mock_user_repo.find_by_email.return_value = None
        user_data = CreateUserSchema(
                first_name="James",
                last_name="Glory",
                email="jamesglory1@gmail.com",
                password="password123!",
                confirm_password="password123!",
            )
        with pytest.raises(ValueError) as exc_info:
            user_service.register(user_data)
        assert "uppercase letter" in str(exc_info.value).lower()


def test_register_weak_password_no_digit(mock_user_repo, user_service):
    mock_user_repo.find_by_email.return_value = None
    user_data = CreateUserSchema(
        first_name="James",
        last_name="Glory",
        email="jamesglory1@gmail.com",
        password="Password!",
        confirm_password="Password!",
    )
    with pytest.raises(ValueError) as exc_info:
        user_service.register(user_data)
    assert "digit" in str(exc_info.value).lower()


def test_register_weak_password_no_special_char(mock_user_repo, user_service):
    mock_user_repo.find_by_email.return_value = None
    user_data = CreateUserSchema(
        first_name="James",
        last_name="Glory",
        email="jamesglory1@gmail.com",
        password="Password123",
        confirm_password="Password123",
    )
    with pytest.raises(ValueError) as exc_info:
        user_service.register(user_data)
    assert "special character" in str(exc_info.value).lower()


def test_register_password_mismatch(user_service):
    with pytest.raises(ValidationError) as exc_info:
        CreateUserSchema(
            first_name="James",
            last_name="Glory",
            email="jamesglory1@gmail.com",
            password="Password123!",
            confirm_password="Password456!",
        )
    assert "don't match" in str(exc_info.value).lower()


def test_register_existing_email(mock_user_repo, user_service, sample_user):
    mock_user_repo.find_by_email.return_value = sample_user
    user_data = CreateUserSchema(
        first_name="John",
        last_name="Smith",
        email="johnsmith1@gmail.com",
        password="LamineYamal10!",
        confirm_password="LamineYamal10!"
    )
    with pytest.raises(ValueError) as exc_info:
        user_service.register(user_data)
    assert "already exists" in str(exc_info.value).lower()


def test_login_success(mock_user_repo, user_service, sample_user):
    mock_user_repo.find_by_email.return_value = sample_user
    login_data = LoginUserSchema(
        email="johnsmith1@gmail.com",
        password="LamineYamal10!",
    )
    result = user_service.login_user(login_data)
    assert result.email == "johnsmith1@gmail.com"
    assert result.is_verified is True
    mock_user_repo.find_by_email.assert_called_once_with("johnsmith1@gmail.com")


def test_login_unverified_user(mock_user_repo, user_service, unverified_user):
    mock_user_repo.find_by_email.return_value = unverified_user
    login_data = LoginUserSchema(
        email="gabisam123@gmail.com",
        password="Lewyword10!",
    )
    with pytest.raises(ValueError) as exc_info:
        user_service.login_user(login_data)
    assert "not been verified" in str(exc_info.value).lower()


def test_login_user_not_found(mock_user_repo, user_service):
    mock_user_repo.find_by_email.return_value = None
    login_data = LoginUserSchema(
        email="nonexistent@gmail.com",
        password="LamineYamal11!",
    )
    with pytest.raises(ValueError) as exc_info:
        user_service.login_user(login_data)
    assert "not found" in str(exc_info.value).lower()


def test_login_incorrect_password(mock_user_repo, user_service, sample_user):
    mock_user_repo.find_by_email.return_value = sample_user
    login_data = LoginUserSchema(
        email="johnsmith1@gmail.com",
        password="WrongPassword123!",
    )
    with pytest.raises(ValueError) as exc_info:
        user_service.login_user(login_data)
    assert "incorrect password" in str(exc_info.value).lower()


def test_verify_user_success(mock_user_repo, user_service, unverified_user):
    mock_user_repo.find_by_verification_code.return_value = unverified_user
    result = user_service.verify_user("token_abc123")
    assert result is True
    assert unverified_user.is_verified is True
    assert unverified_user.verification_code is None
    mock_user_repo.save.assert_called_once_with(unverified_user)


def test_verify_user_invalid_token(mock_user_repo, user_service):
    mock_user_repo.find_by_verification_code.return_value = None
    with pytest.raises(ValueError) as exc_info:
        user_service.verify_user("invalid_token")
    assert "invalid verification code" in str(exc_info.value).lower()


def test_get_user_by_id_success(mock_user_repo, user_service, sample_user):
    mock_user_repo.find_by_user_id.return_value = sample_user
    result = user_service.get_user_by_id(1)
    assert result is not None
    assert result.id == 1
    assert result.email == "johnsmith1@gmail.com"
    mock_user_repo.find_by_user_id.assert_called_once_with(1)


def test_get_user_by_id_not_found(mock_user_repo, user_service):
    mock_user_repo.find_by_user_id.return_value = None
    result = user_service.get_user_by_id(999)
    assert result is None
    mock_user_repo.find_by_user_id.assert_called_once_with(999)


def test_get_user_by_email_success(mock_user_repo, user_service, sample_user):
    mock_user_repo.find_by_email.return_value = sample_user
    result = user_service.get_user_by_email("johnsmith1@gmail.com")
    assert result is not None
    assert result.email == "johnsmith1@gmail.com"
    mock_user_repo.find_by_email.assert_called_once_with("johnsmith1@gmail.com")


def test_get_user_by_email_not_found(mock_user_repo, user_service):
    mock_user_repo.find_by_email.return_value = None
    result = user_service.get_user_by_email("notfound@gmail.com")
    assert result is None


def test_get_user_by_email_invalid_format(user_service):
    with pytest.raises(ValueError) as exc_info:
        user_service.get_user_by_email("invalid-email")
    assert "invalid email" in str(exc_info.value).lower()


def test_update_user_success(mock_user_repo, user_service, sample_user):
    updated_user = MagicMock()
    updated_user.id = 1
    updated_user.first_name = "Johnny"
    updated_user.last_name = "Smith"
    updated_user.email = "johnsmith1@gmail.com"
    updated_user.role = "BUYER"
    updated_user.is_verified = True
    updated_user.created_at = datetime.now()
    mock_user_repo.update_user.return_value = updated_user
    update_data = {"first_name": "Johnny"}
    result = user_service.update_user(1, update_data)
    assert result.first_name == "Johnny"
    mock_user_repo.update_user.assert_called_once_with(1, update_data)


def test_update_user_not_found(mock_user_repo, user_service):
    mock_user_repo.update_user.return_value = None
    update_data = {"first_name": "Johnny"}
    with pytest.raises(ValueError) as exc_info:
        user_service.update_user(999, update_data)
    assert "not found" in str(exc_info.value).lower()


def test_delete_user_success(mock_user_repo, user_service):
    mock_user_repo.delete_user.return_value = True
    result = user_service.delete_user(1)
    assert result is True
    mock_user_repo.delete_user.assert_called_once_with(1)


def test_delete_user_not_found(mock_user_repo, user_service):
    mock_user_repo.delete_user.return_value = False
    with pytest.raises(ValueError) as exc_info:
        user_service.delete_user(999)
    assert "not found" in str(exc_info.value).lower()