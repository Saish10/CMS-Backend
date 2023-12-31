from app.app import swagger_api
from flask_restx import fields

signup_request_data = swagger_api.model(
    'Signup Post Request Body',
    {
        'email': fields.String(description='Email', required=True),
        'username': fields.String(description='Username', required=True),
        'password': fields.String(description='Password', required=True),
        'first_name': fields.String(description='first_name', required=True),
        'last_name': fields.String(description='last_name', required=True)
    }
)

login_request_data = swagger_api.model(
    'Login Post Request Body',
    {
        'email': fields.String(description='Email', required=True),
        'password': fields.String(description='Password', required=True),
    }
)

logout_request_data = swagger_api.model(
    "Logout Post Request Body",
    {
        'user_id': fields.String(description='User ID', required=True)
    }
)

user_detail_request = {
    'user_id': {
        'description': 'Enter User ID.', 'type': 'string', 'default': None
    },
}