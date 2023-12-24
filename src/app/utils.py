from ulid import new
from app.app import logger, bcrypt
from app.constants import ERROR_MSG
from db.models import User


class Utils:
    @staticmethod
    def generate_ulid():
        return str(new())


class UserManager:

    def __init__(self) -> None:
        super().__init__()

    def signup(self, data):
        try:
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            first_name = data.get("first_name")
            last_name = data.get("last_name")

            user_exists = User.get_user(email=email.lower(), is_active=True)
            username_exists = User.get_user(username=username, is_active=True)
            if user_exists:
                return False, "User already exists"
            if username_exists:
                return False, "Username already exists"

            password = bcrypt.generate_password_hash(password).decode("utf-8")

            signup_data = {
                "username": username,
                "email": email.lower(),
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            }
            success = User.create_user(signup_data)
            if not success:
                return False, "Error in creating user."
            return True, "User has been signed up successfully."
        except Exception as e:
            logger.error(f"UserManager: Error in signup - {e}", exc_info=True)
            return False, ERROR_MSG


class AuthenticationManager:
    pass
