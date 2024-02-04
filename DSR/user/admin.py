from django.contrib import admin
from .models import *

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'isd_code', 'alpha3','alpha2','currency','currency_symbol','currency_code',)
    search_fields = ('name','isd_code','currency','alpha3',)


class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country','iso_code',)
    ordering = ('name',)


class PhoneNumberAdmin(admin.ModelAdmin):
    pass


class RoleAdmin(admin.ModelAdmin):
    pass


class BranchAdmin(admin.ModelAdmin):
    pass


class CompanyProfileAdmin(admin.ModelAdmin):
    pass


class UserAccountAdmin(admin.ModelAdmin):
    pass


class InvitationAdmin(admin.ModelAdmin):
    pass


class InvitationHistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(InvitationHistory, InvitationHistoryAdmin)

