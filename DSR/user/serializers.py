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
    country = serializers.CharField()

class BranchDetailsSerializer(serializers.Serializer):
    branch_name = serializers.CharField()
    branch_address = AddressSerializer()

class CompanySerializer(serializers.Serializer):
    name = serializers.CharField()
    branch_details = BranchDetailsSerializer()

class RoleSerializer(serializers.Serializer):
    role_id = serializers.CharField(allow_null=True, required=False)
    slug = serializers.CharField(allow_null=True, required=False)
    name = serializers.CharField(allow_null=True, required=False)

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
    role = RoleSerializer(required=False)



class AddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PhoneDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'

class RoleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    address = AddressDetailSerializer()
    phone = PhoneDetailSerializer()
    role = RoleDetailSerializer()
    company = CompanyProfileSerializer()
    class Meta:
        model = UserAccount
        fields = ('internal_id', 'email', 'first_name', 'last_name', 'dob',
                  'employee_code', 'role', 'address', 'phone', 'company')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()