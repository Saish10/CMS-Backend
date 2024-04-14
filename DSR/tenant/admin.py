from django.contrib import admin
from .models import *



class TenantAdmin(admin.ModelAdmin):
    list_display = ('internal_id','name', 'slug', 'is_active')


class TenantConfigAdmin(admin.ModelAdmin):
    list_display = ('tenant',)



admin.site.register(Tenant, TenantAdmin)
admin.site.register(TenantConfig, TenantConfigAdmin)
