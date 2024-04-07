from django.db import transaction
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from DSR.utils import api_response
from drf_yasg.utils import swagger_auto_schema
from .models import TaskType, Project
from .serializers import (
    DSRQuerySerializer, StatusReportSerializer, TaskTypeSerializer, ProjectSerializer,
    DSRListSerializer,
    dsr_detail_param
)
from .utils import DSRManager


class DailyStatusReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    msg_header = 'DSR'

    @swagger_auto_schema(request_body=StatusReportSerializer)
    @api_response
    @transaction.atomic
    def post(self, request):
        data = StatusReportSerializer(data=request.data)
        if not data.is_valid():
            return 400, data.errors, {}

        is_success, message = (
            DSRManager(request).create(data.validated_data, request.user)
        )
        if not is_success:
            return 400, message, {}
        return 200, message, {}

    @swagger_auto_schema(request_body=StatusReportSerializer)
    @api_response
    @transaction.atomic
    def put(self, request):
        data = StatusReportSerializer(data=request.data)
        if not data.is_valid():
            return 400, data.errors, {}

        is_success, message = (
            DSRManager(request).update(data.validated_data, request.user)
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


class DSRListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    msg_header = 'DSR List'

    @swagger_auto_schema(query_serializer=DSRQuerySerializer)
    @api_response
    def get(self, request):
        user = request.user
        queryset = DSRManager(request).get_daily_status_report(user)
        if not queryset:
            return 404, "No DSR status reports found", {}
        serializer = DSRListSerializer(queryset, many=True)
        return 200, "DSR list retrieved successfully.", serializer.data

class DSRDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    msg_header = 'DSR Detail'

    @swagger_auto_schema(manual_parameters=dsr_detail_param)
    @api_response
    def get(self, request):
        detail = DSRManager(request).get_dsr_detail()
        if not detail:
            return 404, "No DSR detail found", {}
        serializer = StatusReportSerializer(detail)
        return 200, "DSR detail retrieved successfully.", serializer.data