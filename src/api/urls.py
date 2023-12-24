from app.app import swagger_api
from .views import (
    RegisterView, UserDetailView, LoginView
)


swagger_api.add_resource(RegisterView, '/api/register/')
swagger_api.add_resource(UserDetailView, '/api/user-detail/')
swagger_api.add_resource(LoginView, '/api/user-login/')