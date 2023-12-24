from flask.views import MethodView
from marshmallow import ValidationError, validate
from app.app import swagger_api
from flask_restx import Resource

class RegisterView(Resource, MethodView):
    msg_header = "Sign Up"
    @swagger_api.expect()
    def post(self, *args, **kwargs):
        pass

class UserDetailView(Resource, MethodView):
    msg_header = " User Details"
    def get(self, *args, **kwargs):
        pass

class LoginView(Resource, MethodView):
    msg_header = " User Details"
    def post(self, *args, **kwargs):
        pass