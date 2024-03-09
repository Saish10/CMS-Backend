from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from django.contrib.auth import authenticate
from DSR.utils import api_response
from .utils import (
    UserOnboarding
)
from .serializers import (
    RegisterSerializer
)


class RegisterView(APIView):
    msg_header = 'Register User'

    @api_response
    @transaction.atomic
    def post(self, request):
        """
        Handles the POST request for user registration.

        Validates the incoming data using the `RegisterSerializer` and calls
        the `register_user` method of the `UserOnboarding` class to perform the
        registration process.

        Returns a success message if the registration is successful, or an
        error message if there are any validation errors or registration fails.
        """
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return 400, "error", serializer.errors, {}

        is_success, message = UserOnboarding().register_user(serializer.validated_data)
        if not is_success:
            return 400, "error", message, {}
        return 200, "success", message, {}


class Login(APIView):
    msg_header = 'Login User'
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    @api_response
    def post(self, request):
        """
        Handles the POST request to the login endpoint.
        Authenticates the user with the provided email and password,
        generates a token for the user if authentication is successful,
        and returns the token and user ID in the response.
        """
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if not user:
            return 401, "error", "Invalid credentials", {}

        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user_id': user.internal_id
        }
        return 200, "success", "Login successful", data


class Logout(APIView):
    msg_header = "Logout User"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles the POST request for logging out a user.
        Deletes the token associated with the user from the database.
        Returns a success message.
        """
        user = request.user
        Token.objects.filter(user=user).delete()
        return 200, "success", "Logout successful", {}