from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from DSR.utils import api_response
from .models import (
    Tenant
)
from .serializers import (
    TenantSerializer, tenant_url
)


class TenantDetail(APIView):
    msg_header = 'Tenant Detail'
    @swagger_auto_schema(manual_parameters=tenant_url)
    @api_response
    def get(self, request):
        tenant_url = request.query_params.get('tenant_url')
        if not tenant_url:
            return 400, "error", "Please provide tenant url", {}
        tenant = Tenant.objects.get(url=tenant_url)
        serializer = TenantSerializer(tenant)
        return 200, "details", serializer.data


class TenantList(APIView):
    msg_header = 'Tenant List'

    @api_response
    def get(self, request):
        tenant = Tenant.filter_tenant(is_active=True)
        if tenant is None:
            return 200, "success", "No tenants found", []
        serializer = TenantSerializer(tenant, many=True, context={'exclude_tenant_theme': True})
        return 200, "tenant list retrieved successfully", serializer.data

