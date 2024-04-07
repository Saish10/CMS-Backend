from django.contrib import admin
from .models import *

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ("assigned_users",)  # Assuming "assigned_users" is the many-to-many field

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "assigned_users":  # Replace "assigned_users" with your actual field name
            qs = kwargs.get("queryset", db_field.remote_field.model.objects)
            # Any additional customization you want to apply to the queryset can go here
            kwargs["queryset"] = qs

        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('internal_id','name', 'slug', 'is_active', )

class DailyStatusReportAdmin(admin.ModelAdmin):
    list_display = (
        'internal_id','full_name', 'date', 'task_details',
        'task_type', 'hours_worked', 'project',
    )
    list_filter = ('project',)
    search_fields = ('user__first_name','user__last_name')

    def full_name(self, obj):
        return obj.user.full_name

admin.site.register(Project, ProjectAdmin)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(DailyStatusReport, DailyStatusReportAdmin)