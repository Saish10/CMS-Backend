from django.db import models
from django.utils.translation import gettext_lazy as _
from DSR.utils import BaseModel, ULIDField


class Tenant(BaseModel):

    internal_id = ULIDField(_('tenant id'), editable=False)
    name = models.CharField(_('tenant name'), max_length=100)
    slug = models.SlugField(_('tenant slug'), max_length=100, unique=True)
    url = models.URLField(_('tenant url'), unique=True)


    def __str__(self):
        return self.name

    @classmethod
    def get_tenant(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_tenant(cls, **criteria):
        return cls.objects.filter(**criteria)


class TenantConfig(BaseModel):

    internal_id = ULIDField(_('tenant config id'), editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, related_name='tenant_config')

    def __str__(self):
        return f'Tenant Config: {self.id}'

    @classmethod
    def get_tenant_config(cls, **criteria):
        return cls.objects.get(**criteria)


class TenantTheme(BaseModel):
    internal_id = ULIDField(_('tenant theme id'), editable=False)
    logo = models.ImageField(_('logo'), editable=True, blank=True)
    primary_color = models.CharField(_('primary color'), max_length=10, null=True)
    secondary_color = models.CharField(_('secondary color'), max_length=10, null=True)
    tertiary_color = models.CharField(_('tertiary color'), max_length=10, null=True)
    tenant_tagline = models.TextField(_('tenant tagline'), null=True, db_index=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, related_name='tenant_theme')

    def __str__(self):
        return f'TenantTheme: {self.id}'

    @classmethod
    def get_tenant_theme(cls, **criteria):
        return cls.objects.get(**criteria)