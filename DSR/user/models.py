import uuid
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from DSR.utils import BaseModel, ULIDField, UserAccountManager


class Country(BaseModel):

    internal_id = ULIDField(_('country ulid'), editable = False)
    name = models.CharField(_('country name'), max_length=255)
    isd_code = models.CharField(_('isd code'), max_length=50)
    alpha2 = models.CharField(_('alpha 2'), max_length=100)
    alpha3 = models.CharField(_('apha 3'), max_length=100)
    currency = models.CharField(_('currency'), max_length=100)
    currency_symbol = models.CharField(_('currency symbol'), max_length=100)
    currency_code = models.CharField(_('currency code'), max_length=100)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

    @classmethod
    def filter_country(cls, **criteria):
        return cls.objects.filter(**criteria)

    @classmethod
    def get_country(cls, **criteria):
        return cls.objects.get(**criteria)



class State(BaseModel):

    internal_id = ULIDField(_('state uuid'), editable = False)
    name = models.CharField(_('state name'), max_length=255)
    iso_code = models.CharField(_('iso code'), max_length=2)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.name

    @classmethod
    def get_state(cls, **criteria):
        return cls.objects.filter(**criteria)


class PhoneNumber(BaseModel):

    internal_id = ULIDField(_('phone ulid'), editable = False)
    phone = models.CharField(_('phone number'), blank=True, help_text="phone number")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Phone Number'
        verbose_name_plural = 'Phone Numbers'

    def __str__(self):
        return f"{self.country.isd_code} {self.phone}"

    @classmethod
    def get_phone_number(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_phone_number(cls, **criteria):
        return cls.objects.filter(**criteria)


class Address(BaseModel):

    internal_id = ULIDField(_('address id'), editable=False)
    address_1 = models.CharField(_('address 1'), max_length=100)
    address_2 = models.CharField(_('address 2'), max_length=100)
    zip_code = models.CharField(_('zip code'), max_length=50)
    city = models.CharField(_('city'), max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.address_1

    @classmethod
    def get_address(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_address(cls, **criteria):
        return cls.objects.filter(**criteria)


class Role(BaseModel):

    internal_id = ULIDField(_('role id'), editable=False)
    slug =  models.SlugField(_('role slug'), max_length=100, unique=True, db_index=True)
    name = models.CharField(_('role name'), max_length=100)
    tenant = models.ForeignKey('tenant.Tenant', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name

    @classmethod
    def get_role(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_role(cls, **criteria):
        return cls.objects.filter(**criteria)


class Branch(BaseModel):

    internal_id = ULIDField(_('branch id'), editable=False)
    branch_name = models.CharField(_('branch name'), max_length=100)
    branch_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.branch_name


    @classmethod
    def get_branch(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_branch(cls, **criteria):
        return cls.objects.filter(**criteria)


class CompanyProfile(BaseModel):

    internal_id = ULIDField(_('company id'), editable=False)
    name = models.CharField(_('company name'), max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='company')

    class Meta:
        verbose_name = 'Company Profile'
        verbose_name_plural = 'Company Profiles'

    def __str__(self):
        return self.name

    @classmethod
    def get_company(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_company(cls, **criteria):
        return cls.objects.filter(**criteria)


class UserAccount(AbstractBaseUser, PermissionsMixin, BaseModel):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    internal_id = ULIDField(_('user id'), editable = False)
    email = models.EmailField(_('email'), max_length=255, unique=True)
    secondary_email = models.EmailField(_('secondary email'),max_length=254, help_text="secondary email address")
    first_name = models.CharField(_('first name'),max_length=254, help_text="First Name of the User")
    last_name = models.CharField(_('last name'),max_length=254, help_text="Last Name of the User")
    gender = models.CharField(_('sex'), max_length=6, choices=GENDER_CHOICES)
    dob = models.DateTimeField(_('date of birth'), auto_now_add=True)
    employee_code = models.CharField(_('employee code'), max_length=50)
    joining_date = models.DateField(_('joining date'), auto_now=True)
    address = models.ForeignKey(Address ,on_delete=models.CASCADE, null=True)
    phone = models.ForeignKey(PhoneNumber ,on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, null=True)
    tenant = models.ForeignKey('tenant.Tenant', on_delete=models.CASCADE, null=True)
    is_staff = models.BooleanField(_("is staff"), default=False)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """
        Get the full name of the user.

        Returns:
            str: The full name of the user.
        """
        first_name = self.first_name if self.first_name else ""
        last_name = self.last_name if self.last_name else ""

        return f"{first_name} {last_name}".strip()

    @classmethod
    def get_user(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_user(cls, **criteria):
        return cls.objects.filter(**criteria)

    def save(self, *args, **kwargs):
        if not self.employee_code:
            self.employee_code = self.generate_employee_code()
        super().save(*args, **kwargs)

    def generate_employee_code(self) -> str:
        """
        Generates an employee code for a user based on their company name and a unique identifier.

        Returns:
            str: The generated employee code for the user.
        """
        if self.company:
            prefix = slugify(self.first_name).upper()
        else:
            prefix = "EMP"
        unique_id = str(uuid.uuid4().int)[:4]
        employee_code = f"{prefix}-{unique_id}"
        return employee_code


class Invitation(BaseModel):

    internal_id = ULIDField(_('invitation id'), editable = False)
    inviter_id = models.ForeignKey(UserAccount,  on_delete=models.CASCADE, related_name='invitations')
    first_name = models.CharField(_('first name'), max_length=254)
    last_name = models.CharField(_('last name'), max_length=254)
    email = models.EmailField(_('email'), max_length=255, unique=True)
    role = models.ForeignKey(Role,  on_delete=models.CASCADE, related_name='invitations')
    tenant = models.ForeignKey('tenant.Tenant', on_delete=models.CASCADE, related_name='invitations')

    class Meta:
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'

    @classmethod
    def get_invitation(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_invitation(cls, **criteria):
        return cls.objects.filter(**criteria)


class InvitationHistory(BaseModel):

    internal_id = ULIDField(_('invitation id'), editable = False)
    email = models.EmailField(_('email'), max_length=255, unique=False)
    token = models.TextField()
    expiry_date = models.DateTimeField(_('expires at'))

    class Meta:
        verbose_name = 'Invitation History'
        verbose_name_plural = 'Invitation History'

    @classmethod
    def get_invitation_history(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_invitation_history(cls, **criteria):
        return cls.objects.filter(**criteria)
