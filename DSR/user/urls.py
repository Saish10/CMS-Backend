from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    # Todo
    # path('details/', RegisterView.as_view(), name='details'),
    # path('list/', RegisterView.as_view(), name='list'),
]

