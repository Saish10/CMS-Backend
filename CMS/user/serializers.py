from rest_framework import serializers
from .models import *
from CMS.utils import ModelSerializer
from drf_yasg import openapi

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
    registration_number = serializers.CharField()
    company_type = serializers.CharField()
    company_email = serializers.EmailField()
    company_phone = serializers.CharField()
    incorporation_date = serializers.DateField()

class RoleSerializer(serializers.Serializer):
    role_id = serializers.CharField(allow_null=True, required=False)
    slug = serializers.CharField(allow_null=True, required=False)
    name = serializers.CharField(allow_null=True, required=False)

class RegisterSchema(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    company_details = CompanySerializer()
    branch_details = BranchDetailsSerializer()
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

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields =('name', 'isd_code', 'alpha2', 'alpha3', 'currency',
                 'currency_symbol', 'currency_code')


class StateSerializer(ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = State
        fields = ('name', 'country')


class AddressDetailSerializer(ModelSerializer):
    state = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    class Meta:
        model = Address
        fields = ('address_1', 'zip_code', 'city', 'state', 'country')

    def get_country(self, obj):
        return obj.country.name

    def get_state(self, obj):
        return obj.state.name


class PhoneDetailSerializer(ModelSerializer):
    isd_code = serializers.SerializerMethodField()
    class Meta:
        model = PhoneNumber
        fields = ('phone', 'isd_code')

    def get_isd_code(self, obj):
        return obj.country.isd_code


class RoleDetailSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('internal_id', 'slug', 'name')


class BranchSerializer(ModelSerializer):
    branch_address = AddressDetailSerializer()
    class Meta:
        model = Branch
        fields = ('branch_name', 'branch_address')



class CompanyProfileSerializer(ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = ('name', 'registration_number')


class UserDetailSerializer(ModelSerializer):
    address = AddressDetailSerializer()
    phone = PhoneDetailSerializer()
    role = RoleDetailSerializer()
    company = CompanyProfileSerializer()
    branch = BranchSerializer()
    class Meta:
        model = UserAccount
        fields = ('internal_id', 'email', 'first_name', 'last_name', 'dob',
                  'employee_code', 'role', 'address', 'phone', 'company',
                  'branch')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values for the fields if they are not provided
        self.fields['email'].default = 'sn.saishnaik@gmail.com'
        self.fields['password'].default = 'dsr@123'


class UserListSerializer(ModelSerializer):
    branch = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    class Meta:
        model = UserAccount
        fields = ('full_name', 'email', 'employee_code', 'role', 'branch')

    
    def get_branch(self, obj):
        return obj.branch.branch_name
    
    def get_role(self, obj):
        return obj.role.name


class UserQuerySerializer(serializers.Serializer):
    role = serializers.CharField(required=False)
    branch = serializers.CharField(required=False)
    q=serializers.CharField(required=False)






""" PARAMETERS FOR GET API REQUESTS. """

branch_list_param=[
    openapi.Parameter(
        'company_id',
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=True,
    ),
]