from rest_framework import serializers
from CMS.utils import ModelSerializer
from .models import Project, TaskType, DailyStatusReport
from drf_yasg import openapi

class StatusReportSerializer(serializers.Serializer):
    internal_id = serializers.CharField(required=False)
    date = serializers.DateField()
    task = serializers.CharField()
    status_summary = serializers.CharField()
    hours_worked = serializers.DecimalField(max_digits=5, decimal_places=2)
    task_type = serializers.CharField()
    project = serializers.CharField()


class TaskTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskType
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class DSRListSerializer(ModelSerializer):
    project = serializers.SerializerMethodField()
    task_type = serializers.SerializerMethodField()
    class Meta:
        model = DailyStatusReport
        fields = (
            'internal_id', 'date', 'project', 'task', 'hours_worked',
            'task_type'
        )

    def get_task_type(self, obj):
        return obj.task_type.name

    def get_project(self, obj):
        return obj.project.name

class DSRQuerySerializer(serializers.Serializer):
    date = serializers.DateField(required=False)
    month_year = serializers.CharField(required=False)
    project = serializers.CharField(required=False)



""" PARAMETERS FOR GET API REQUESTS. """

dsr_detail_param=[
    openapi.Parameter(
        'internal_id',
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=True,
    ),
]