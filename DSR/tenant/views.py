from DSR.utils import api_response
from rest_framework.generics import RetrieveAPIView
from .models import Tenant
from .serializers import TenantSerializer
from rest_framework.views import APIView


class TenantDetail(APIView):
    msg_header = 'Tenant Detail'
    @api_response
    def get(self, request):
        tenant_url = request.query_params.get('tenant_url')
        if not tenant_url:
            return 400, "error", "Please provide tenant url", {}
        tenant = Tenant.objects.get(url=tenant_url)
        serializer = TenantSerializer(tenant)
        return 200, "success", "details", serializer.data


class TenantList(APIView):
    msg_header = 'Tenant List'

    @api_response
    def get(self, request):
        tenant = Tenant.filter_tenant(is_active=True)
        if tenant is None:
            return 200, "success", "No tenants found", []
        serializer = TenantSerializer(tenant, many=True, context={'exclude_tenant_theme': True})
        return 200, "success", "tenant list retrieved successfully", serializer.data

