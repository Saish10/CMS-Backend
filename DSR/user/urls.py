from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # Todo
    # path('login/', RegisterView.as_view(), name='login'),
    # path('logout/', RegisterView.as_view(), name='logout'),
    # path('details/', RegisterView.as_view(), name='details'),
    # path('list/', RegisterView.as_view(), name='list'),
]