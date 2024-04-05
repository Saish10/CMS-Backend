from django.contrib import admin
from .models import *
from worklog.models import Project

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'isd_code', 'alpha3','alpha2','currency','currency_symbol','currency_code',)
    search_fields = ('name','isd_code','currency','alpha3',)


class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country','iso_code',)
    list_filter = ('country',)
    ordering = ('name',)


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('isd_code', 'phone', 'country')

    def isd_code(self, obj):
        return obj.country.isd_code
    isd_code.short_description = 'ISD Code'


class RoleAdmin(admin.ModelAdmin):
    list_display = ('internal_id','name', 'slug','tenant','is_active', )


class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'branch_address', 'city', 'state',)

    def city(self, obj):
        return obj.branch_address.city

    def state(self, obj):
        return obj.branch_address.state


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_email','registration_number')



class ProjectFilter(admin.SimpleListFilter):
    title = 'Project'
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        projects = Project.objects.all()
        return [(project.id, project.name) for project in projects]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(assigned_projects__id=self.value())


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'employee_code', 'company', 'role', 'is_active')
    list_filter = ('role', 'company', ProjectFilter, 'is_active')




class InvitationAdmin(admin.ModelAdmin):
    pass


class InvitationHistoryAdmin(admin.ModelAdmin):
    pass

class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_1', 'zip_code','city','state','country')


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(InvitationHistory, InvitationHistoryAdmin)

