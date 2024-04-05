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
    RegisterSerializer, UserSerializer, UserLoginSerializer,
    UserListSerializer
)
from .models import (
    UserAccount
)
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class RegisterView(APIView):
    msg_header = 'Register User'

    @swagger_auto_schema(request_body=RegisterSerializer)
    @api_response
    @transaction.atomic
    def post(self, request):
        """
        Handles the POST request for user registration.

        """
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return 400, "error", serializer.errors, {}

        is_success, message = UserOnboarding().register_user(serializer.validated_data)
        if not is_success:
            return 400, message, {}
        return 200, message, {}


class Login(APIView):
    msg_header = 'Login User'
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]


    @swagger_auto_schema(request_body=UserLoginSerializer)
    @api_response
    def post(self, request):
        """
        Handles the POST request to the login endpoint.

        """
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if not user:
            return 401, "Invalid credentials", {}

        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user_id': user.internal_id
        }
        return 200, "Login successful", data


class Logout(APIView):
    msg_header = "Logout User"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # @method_decorator(csrf_exempt, name='dispatch')
    @api_response
    def post(self, request):
        """
        Handles the POST request for logging out a user.
        """
        user = request.user
        Token.objects.filter(user=user).delete()
        return 200, "Logout successful", {}


class UserDetails(APIView):
    msg_header = "User Details"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @api_response
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return 200, "User details retrieved successfully", serializer.data


class UserList(APIView):
    msg_header = "User List"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @api_response
    def get(self, request):
        tenant = request.user.tenant
        user_list = UserAccount.get_user_list(tenant)
        if not user_list:
            return 200, "No Data Found", []
        serializer = UserListSerializer(many=True)
        return 200, "User details retrieved successfully", serializer.data
