import jwt
from flask import jsonify, make_response, request
from ulid import new
from app.app import logger, bcrypt, db, app
from app.constants import ERROR_MSG
from app.settings import TOKEN_EXPIRATION
from db.models import (AuthToken, User)
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import desc
from datetime import  timedelta, datetime
current_time =datetime.now()

def api_response(api_function):
    @wraps(api_function)
    def wrapper(request, *args, **kwargs):
        msg_header = request.msg_header
        method_type = api_function.__name__.upper()
        try:
            status_code, status, message, extra = api_function(request, *args, **kwargs)
            return Utils.get_api_response(status_code, status,
                                          msg_header, message, data=extra)
        except Exception as e:
            logger.error(f"{method_type} API | Error: {e}", exc_info=True)
            return Utils.get_api_response(400, msg_header, str(e), "error", None)

    return wrapper

def login_required(api_function):
    @wraps(api_function)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return 401, "error", "Authentication", "Token missing"

        token = request.headers.get('Authorization').split(' ')[1]
        user_id = AuthenticationManager().decode_token(token)
        print(user_id, "Authent")
        if user_id is None:
            return 401, "error", "Authentication", "Invalid token"

        kwargs['current_user'] = user_id
        return api_function(*args, **kwargs)

    return wrapper

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

    @staticmethod
    def get_api_response(status_code, status, message_header, message, data=None):
        response = {
            "status_code": status_code,
            "status": status,
            "message_header": message_header,
            "message": message,
        }
        if data is not None:
            response["data"] = data

        return make_response(jsonify(response))


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

            user_exists = User.get_user(
                email=email.lower(), is_active=True).first()
            username_exists = User.get_user(
                username=username, is_active=True).first()
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

    def get_user_details(self, user_id):
        try:
            user = User.get_user(user_id=user_id, is_active=True).first()
            if not user:
                return False, "User not found.", None
            return True, "User details retrieved successfully.", user
        except Exception as e:
            logger.error(
                f"UserManager: Error in get_user_details - {e}", exc_info=True)
            return False, ERROR_MSG, None

    def get_user_list(self, args):
        try:
            user_list = User.get_user()
            if not user_list:
                return False, "No users found.", []
            return True, "User list retrieved successfully.", user_list
        except Exception as e:
            logger.error(
                f"UserManager: Error in get_user_list - {e}", exc_info=True)
            return False, ERROR_MSG, []


class AuthenticationManager:
    def __init__(self) -> None:
        super().__init__()

    def authenticate(self, data):
        try:

            email = data.get("email", None)
            password = data.get("password", None)

            if email:
                user = User.get_user(email=email).first()
                if not user:
                    return False, "Login Credentials are incorrect."

            if not self.validate_password(user.password, password):
                return False, "Your login credential are incorrect."

            if not user.is_active:
                return False, "Your account has been disabled."

            extra_data = self.generate_token(user.user_id)

            return True, "Successfully logged in.", extra_data
        except Exception as e:
            logger.error(
                f"AuthManager: Error in authenticate - {e}", exc_info=True)
            return False, ERROR_MSG, None

    def validate_password(self, password_hash, raw_password):
        return bcrypt.check_password_hash(password_hash, raw_password)

    def logout(self, user_id):
        try:
            print(user_id)
            AuthToken.query.filter(
                (AuthToken.user_id == user_id)
                ).update(dict(is_active=False))

            db.session.flush()
            return True, "Successfully logged out."
        except Exception as e:
            logger.error(f"AuthManager: Error in logout - {e}", exc_info=True)
            return False, ERROR_MSG

    def decode_token(self, token):
        try:
            payload = jwt.decode(token,
                                 app.config['SECRET_KEY'],
                                 algorithms=['HS256'])
            return payload['sub']
        except Exception as e:
            logger.error(
                f"AuthManager: Error in decode_token - {e}", exc_info=True)
            return None

    def generate_token(self, user_id):
        try:
            payload = {
                'exp': current_time + timedelta(minutes=TOKEN_EXPIRATION),
                'sub': user_id
            }
            token = jwt.encode(
                payload, app.config['SECRET_KEY'], algorithm='HS256')
            auth_token = AuthToken(user_id=user_id, token=token)
            db.session.add(auth_token)
            db.session.flush()
            return token
        except Exception as e:
            logger.error(
                f"AuthManager: Error in generate_token - {e}", exc_info=True)
            return None
