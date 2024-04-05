from rest_framework import serializers

from .models import Project, TaskType


class StatusReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    task_details = serializers.CharField()
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