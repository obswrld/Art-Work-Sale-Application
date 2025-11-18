class ServiceError(Exception):
    pass

class InvalidEmailCredentials(ServiceError):
    def __init__(self, email: str):
        super().__init__(f"Invalid email credentials{email}")
        self.email = email

class InvalidPasswordCredentials(ServiceError):
    def __init__(self, message="Invalid password, does not meet the proper requirements"):
        super().__init__(message)

class MissingRequiredField(ServiceError):
    def __init__(self, field_name: str):
        super().__init__(f"Missing required field {field_name}")
        self.field_name = field_name

class UserAlreadyExists(ServiceError):
    def __init__(self, email: str):
        super().__init__(f"User {email} already exists")
        self.email = email

class UserNotFound(ServiceError):
    def __init__(self, email: str):
        super().__init__(f"User {email} not found")
        self.email = email

class CredentialsMissMatchError(ServiceError):
    def __init__(self):
        super().__init__("Incorrect password for given mail")