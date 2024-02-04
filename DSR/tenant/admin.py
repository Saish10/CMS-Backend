from django.contrib import admin
from .models import *


class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active',)


class TenantThemeAdmin(admin.ModelAdmin):
    pass


class TenantConfigAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tenant, TenantAdmin)
admin.site.register(TenantTheme, TenantThemeAdmin)
admin.site.register(TenantConfig, TenantConfigAdmin)
