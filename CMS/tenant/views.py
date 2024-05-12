from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from CMS.utils import api_response
from .models import (
    Tenant, TenantConfig
)
from .serializers import (
    tenant_url, TenantSerializer
)


class TenantDetail(APIView):
    msg_header = 'Tenant Detail'
    @swagger_auto_schema(manual_parameters=tenant_url)
    @api_response
    def get(self, request):
        tenant_url = request.query_params.get('tenant_url')
        if not tenant_url:
            return 400, "error", "Please provide tenant url", {}
        tenant = TenantConfig.objects.get(url=tenant_url)
        serializer = TenantSerializer(tenant)
        return 200, "details", serializer.data




