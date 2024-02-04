from rest_framework import serializers
from .models import *


class AddressSerializer(serializers.Serializer):
    address_1 = serializers.CharField()
    address_2 = serializers.CharField()
    zip_code = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    isd_code = serializers.CharField()
    country = serializers.CharField()

class CountrySerializer(serializers.Serializer):
    name = serializers.CharField()
    isd_code = serializers.CharField()
    alpha2 = serializers.CharField()
    alpha3 = serializers.CharField()
    currency = serializers.CharField()
    currency_symbol = serializers.CharField()
    currency_code = serializers.CharField()

class StateSerializer(serializers.Serializer):
    name = serializers.CharField()
    country = CountrySerializer()

class CompanySerializer(serializers.Serializer):
    name = serializers.CharField()
    branch = serializers.CharField()
    company_address = AddressSerializer()

class RoleSerializer(serializers.Serializer):
    internal_id = serializers.CharField(allow_null=True)
    name = serializers.CharField()
    slug = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    company_details = CompanySerializer()
    phone_details = PhoneNumberSerializer()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    secondary_email = serializers.EmailField()
    gender = serializers.CharField()
    dob = serializers.DateField()
    joining_date = serializers.DateField()
    address = AddressSerializer()
    tenant_id = serializers.CharField()
    role = RoleSerializer()
