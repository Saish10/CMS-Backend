from functools import wraps
from rest_framework import status
import logging
from django.http import JsonResponse
import json
from django.db import models
from django.utils import timezone
from ulid import new as ulid_new
from django.contrib.auth.models import (
    BaseUserManager
)

logger = logging.getLogger()

class ULIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 26
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value:
            value = str(ulid_new())
            setattr(model_instance, self.attname, value)
        return super().pre_save(model_instance, add)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now, editable=False)
    date_modified = models.DateTimeField(default=timezone.now, editable=True)
    created_by = models.CharField(max_length=500, blank=True)
    updated_by = models.CharField(max_length=500, blank=True)

class UserAccountManager(BaseUserManager):

    def create_user(self, email=None, password=None, **extra_fields):
        try:
            extra_fields.setdefault("is_staff", False)
            extra_fields.setdefault("is_superuser", False)
            if not email:
                raise ValueError('The Email field must be set')
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            return user
        except Exception as e:
            logger.error(f"UserAccountManager | Error in create_user {e}", exc_info=True)
            return None

    def create_superuser(self, email, password=None, **extra_fields):
        try:
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)

            if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_staff=True.')
            if extra_fields.get('is_superuser') is not True:
                raise ValueError('Superuser must have is_superuser=True.')

            user = self.create_user(email, password, **extra_fields)
            user.first_name = "SuperUser"
            return user.save()
        except Exception as e:
            logger.error(f"UserAccountManager | Error in create_superuser {e}", exc_info=True)
            return None

def api_response(api_function):
    @wraps(api_function)
    def wrapper(request, *args, **kwargs):
        msg_header = request.msg_header
        method_type = api_function.__name__.upper()
        try:
            status_code, message, extra = api_function(request, *args, **kwargs)
            return Utils().get_api_response(status_code, msg_header, message, extra)
        except Exception as e:
            logger.error(f"{method_type} API | Error: {e}", exc_info=True)
            return Utils().get_api_response(500, str(e), msg_header, None)

    return wrapper



class Utils:

    def __init__(self):
        super().__init__()

    def get_user_ip_address(self, request):
        try:
            if request and request.META.get('HTTP_X_FORWARDED_FOR'):
                return request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
            return request.META.get('REMOTE_ADDR')

        except Exception as e:
            logger.error(f'Utils | Error in getting user IP address: {e}', exc_info=True)

    def get_user_agent(self, request):
        try:
            user_agent = request.META['HTTP_USER_AGENT']
            return user_agent if user_agent else ''
        except Exception as e:
            logger.error(f'Utils | Error in getting user agent: {e}', exc_info=True)


    def get_api_response(self, status_code, message_header, message, data=None):
        response = {
            "status_code": status_code,
            # "status": status,
            "message_header": message_header,
            "message": message,
        }
        if data is not None:
            response["data"] = data

        return JsonResponse(response)