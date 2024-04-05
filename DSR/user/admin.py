from django.contrib import admin
from rest_framework.authtoken.models import Token
from .models import *

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'isd_code', 'alpha3','alpha2','currency','currency_symbol','currency_code',)
    search_fields = ('name','isd_code','currency','alpha3',)


class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country','iso_code',)
    ordering = ('name',)


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('isd_code', 'phone', 'country')

    def isd_code(self, obj):
        return obj.country.isd_code
    isd_code.short_description = 'ISD Code'


class RoleAdmin(admin.ModelAdmin):
    list_display = ('internal_id','name', 'slug','tenant','is_active', )


class BranchAdmin(admin.ModelAdmin):
    pass


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_email','registration_number')

    def branch_address(self, obj):
        return obj.branch.branch_address if obj.branch else '-'



class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'employee_code', 'company', 'role', 'is_active')


class InvitationAdmin(admin.ModelAdmin):
    pass


class InvitationHistoryAdmin(admin.ModelAdmin):
    pass

class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_1', 'zip_code','city','state','country')


admin.site.register(Token)
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

