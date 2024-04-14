from django.urls import path
from .views import *

urlpatterns = [
    path('detail/', TenantDetail.as_view()),
]