from django.db import transaction
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from DSR.utils import api_response
from .serializers import StatusReportSerializer
from .models import DailyStatusReport


class DailyStatusReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    msg_header = 'DSR'
    @api_response
    @transaction.atomic
    def post(self, request):
        data = StatusReportSerializer(data=request.data)
        if not data.is_valid():
            return 400, "error", data.errors, {}

        is_success, message = (
            DailyStatusReport.create(data.validated_data, request.user)
        )
        if not is_success:
            return 400, message, {}
        return 200, message, {}
