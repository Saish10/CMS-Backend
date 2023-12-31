from app.app import swagger_api
from .views import (
    RegisterView, UserDetailView, LoginView, LogoutView, UserListView
)


swagger_api.add_resource(RegisterView, '/api/register/')
swagger_api.add_resource(LoginView, '/api/login/')
swagger_api.add_resource(LogoutView, '/api/logout/')
swagger_api.add_resource(UserDetailView, '/api/user-detail/')
swagger_api.add_resource(UserListView, '/api/user-list/')
