from django.contrib import admin
from .models import *


class TenantAdmin(admin.ModelAdmin):
    list_display = ('internal_id','name', 'slug', 'is_active', 'url')


class TenantThemeAdmin(admin.ModelAdmin):
    list_display = ('internal_id','primary_color', 'secondary_color', 'tertiary_color', 'tenant')


class TenantConfigAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tenant, TenantAdmin)
admin.site.register(TenantTheme, TenantThemeAdmin)
admin.site.register(TenantConfig, TenantConfigAdmin)
