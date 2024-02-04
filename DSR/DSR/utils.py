from functools import wraps
from rest_framework import status
import logging
from django.http import JsonResponse
import json
from django.db import models
from django.utils import timezone
from ulid import new as ulid_new

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

def api_response(api_function):
    @wraps(api_function)
    def wrapper(request, *args, **kwargs):
        msg_header = request.msg_header
        method_type = api_function.__name__.upper()
        try:
            status_code, status, message, extra = api_function(request, *args, **kwargs)
            return Utils().get_api_response(status_code, status, msg_header, message, extra)
        except Exception as e:
            logger.error(f"{method_type} API | Error: {e}", exc_info=True)
            return Utils().get_api_response(500, msg_header, str(e), 'error', None)

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


    def get_api_response(self, status_code, status, message_header, message, data=None):
        response = {
            "status_code": status_code,
            "status": status,
            "message_header": message_header,
            "message": message,
        }
        if data is not None:
            response["data"] = data

        return JsonResponse(response)