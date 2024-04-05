from django.db import transaction
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from DSR.utils import api_response
from .models import DailyStatusReport, TaskType, Project
from .serializers import (
    StatusReportSerializer, TaskTypeSerializer, ProjectSerializer
)


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


class TaskCategoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    msg_header = 'Task Types List'

    @api_response
    def get(self, request):
        queryset = TaskType().get_task_type_list()
        if not queryset:
            return 200, 'Task categories not found', {}
        serializer = TaskTypeSerializer(queryset, many=True)
        return 200, "Task category list retrieved successfully.", serializer.data


class ProjectsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    msg_header = 'Projects List'

    @api_response
    def get(self, request):
        tenant = request.user.tenant
        queryset = Project().get_project_list(tenant)
        if not queryset:
            return 200, "Projects not found", {}
        serializer = ProjectSerializer(queryset, many=True)
        return 200, "Project list retrieved successfully.", serializer.data