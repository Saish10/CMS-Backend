from django.contrib import admin
from .models import *

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    pass

class TaskTypeAdmin(admin.ModelAdmin):
    pass

class DailyStatusReportAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(DailyStatusReport, DailyStatusReportAdmin)