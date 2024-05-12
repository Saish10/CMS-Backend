from django.urls import path
from .views import *

urlpatterns = [
    path('dsr/', DailyStatusReportView.as_view(), name='dsr'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('task-types/', TaskCategoryView.as_view(), name='task-types'),
    path('dsr-list/', DSRListView.as_view(), name='dsr-list'),
    path('dsr-detail/', DSRDetailView.as_view(), name='dsr-detail'),
]