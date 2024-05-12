from rest_framework import serializers
from drf_yasg import openapi
from .models import TenantConfig


class TenantSerializer(serializers.ModelSerializer):
    tenant_name = serializers.SerializerMethodField()
    class Meta:
        model = TenantConfig
        fields = (
            'internal_id', 'logo', 'primary_color', 'secondary_color',
            'tertiary_color', 'tagline', 'tenant_name'
        )

    def get_tenant_name(self, obj):
        return obj.tenant.name





""" PARAMETERS FOR GET API REQUESTS. """

tenant_url=[
    openapi.Parameter(
        'tenant_url',
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=True,
    ),
]