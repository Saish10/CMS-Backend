from flask.views import MethodView
from flask import request
from flask_restx import Resource
from marshmallow import ValidationError
from app.app import swagger_api
from app.utils import (
    UserManager,
    api_response, commit
    )

from .serializers import (
    RegisterSchema
    )

from .swagger import (
    signup_request_data
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


class UserDetailView(Resource, MethodView):
    msg_header = " User Details"
    @api_response
    def get(self, *args, **kwargs):
        pass

class LoginView(Resource, MethodView):
    msg_header = " User Details"
    @api_response
    def post(self, *args, **kwargs):
        pass