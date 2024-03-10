from rest_framework import serializers
from drf_yasg import openapi
from .models import TenantTheme, Tenant

class TenantThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantTheme
        fields = ['internal_id','primary_color', 'secondary_color', 'tertiary_color', 'tenant_tagline', 'logo']


class TenantSerializer(serializers.ModelSerializer):
    tenant_theme = serializers.SerializerMethodField()
    class Meta:
        model = Tenant
        fields = ['internal_id', 'name', 'slug', 'tenant_theme']

    def get_tenant_theme(self, obj):
        tenant_theme_instance = obj.tenant_theme.first()
        if tenant_theme_instance:
            return TenantThemeSerializer(tenant_theme_instance).data
        return {
            'primary_color': None,
            'secondary_color': None,
            'tertiary_color': None,
            'tenant_tagline': None
        }

    def to_representation(self, instance):
        # Check if the request has a specific parameter to exclude tenant_theme
        exclude_tenant_theme = self.context.get('exclude_tenant_theme', False)

        # If exclude_tenant_theme is True, remove the tenant_theme field from the representation
        if exclude_tenant_theme:
            representation = super().to_representation(instance)
            representation.pop('tenant_theme', None)
            return representation

        return super().to_representation(instance)



""" PARAMETERS FOR GET API REQUESTS. """

tenant_url=[
    openapi.Parameter(
        'tenant_url',
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=True,
    ),
]