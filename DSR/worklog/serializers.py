from rest_framework import serializers


class StatusReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    task_details = serializers.CharField()
    status_summary = serializers.CharField()
    hours_worked = serializers.DecimalField(max_digits=5, decimal_places=2)
    task_type = serializers.CharField()
    project = serializers.CharField()
