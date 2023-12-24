from flask import jsonify
from ulid import new
from app.app import logger, bcrypt, db
from app.constants import ERROR_MSG
from db.models import User
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import desc

def api_response(api_function):
    @wraps(api_function)
    def wrapper(request, *args, **kwargs):
        msg_header = request.msg_header
        method_type = api_function.__name__.upper()
        try:
            status_code, status, message, extra = api_function(request, *args, **kwargs)
            return get_api_response(status_code, status, msg_header, message, extra)
        except Exception as e:
            logger.error(f"{method_type} API | Error: {e}", exc_info=True)
            return get_api_response(400, msg_header, str(e), 'error', None)
    return wrapper

def get_api_response(status_code, status, message_header, message, data=None):
    response = {
        "status_code": status_code,
        "status": status,
        "message_header": message_header,
        "message": message,
    }
    if data is not None:
        response["data"] = data

    return jsonify(response)

def commit(success):
    try:
        if not success:
            db.session.rollback()
            return False
        db.session.commit()
        logger.info("Transaction committed successfully")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error while committing transaction, rolling back: {e}")
        db.session.rollback()
        return False

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

            user_exists = User.get_user(email=email.lower(),
                                        is_active=True).first()
            username_exists = User.get_user(username=username,
                                            is_active=True).first()
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
            success = User.create_user(**signup_data)
            if not success:
                return False, "Error in creating user."
            return True, "User has been signed up successfully."
        except Exception as e:
            logger.error(f"UserManager: Error in signup - {e}", exc_info=True)
            return False, ERROR_MSG


class AuthenticationManager:
    pass
