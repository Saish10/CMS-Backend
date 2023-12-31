from flask.views import MethodView
from flask import request
from flask_restx import Resource
from marshmallow import ValidationError
from app.app import swagger_api
from app.utils import (
    AuthenticationManager, UserManager,
    api_response, commit, login_required
    )

from .serializers import (
    RegisterSchema, UserDetailSerializer
    )

from .swagger import (
    signup_request_data, login_request_data, logout_request_data,
    user_detail_request
)


class RegisterView(Resource, MethodView):
    msg_header = "Sign Up"

    @api_response
    @swagger_api.expect(signup_request_data)
    def post(self, *args, **kwargs):
        try:
            validated_data = RegisterSchema().load(request.get_json())
        except ValidationError as e:
            return 400, "error", e.messages, {}

        success, message = UserManager().signup(validated_data)
        if not success:
            return 400, "error", message, {}
        commit(success)
        return 200, "success", message, {}


class LoginView(Resource, MethodView):
    msg_header = " Login"

    @api_response
    @swagger_api.expect(login_request_data)
    def post(self):
        data = request.get_json()
        success, message, extra = AuthenticationManager().authenticate(data)
        if not success:
            return 400, "error", message, {}
        commit(success)
        return 200, "success", message, extra


class LogoutView(Resource, MethodView):
    msg_header = "Logout"

    @swagger_api.expect(logout_request_data)
    @api_response
    @login_required
    def post(self, *args, **kwargs):
        current_user = kwargs.get('current_user', {})
        success, message = AuthenticationManager().logout(current_user)
        if not success:
            return 400, "error", message, {}
        commit(success)
        return 200, "success", message, {}


class UserDetailView(Resource, MethodView):
    msg_header = "User Detail"

    @swagger_api.doc(params=user_detail_request)
    @api_response
    @login_required
    def get(self):
        user_id = request.args.get('user_id', {})
        success, message, user = UserManager().get_user_details(user_id)
        if not success or not user:
            return 400, "error", message, {}
        data = UserDetailSerializer().dump(user)
        return 200, "success", message, data


class UserListView(Resource, MethodView):
    msg_header = "User List"

    @api_response
    @login_required
    def get(self, *args, **kwargs):
        args = request.args
        success, message, users = UserManager().get_user_list(args)
        if not success:
            return 400, "error", message, {}
        if not users:
            return 200, "success", message, []

        data = UserDetailSerializer(many=True).dump(users)
        return 200, "success", message, data
