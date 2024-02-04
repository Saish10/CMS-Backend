from django.db import transaction
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from DSR.utils import api_response, logger
from .utils import UserOnboarding
from .serializers import RegisterSerializer


class RegisterView(APIView):
    msg_header = 'Register User'
    @api_response
    @transaction.atomic
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return 400, "error", serializer.errors, {}

        is_success, message = UserOnboarding().register_user(serializer.validated_data)
        if not is_success:
            return 400, "error", message, {}
        return 200, "success", message, {}
