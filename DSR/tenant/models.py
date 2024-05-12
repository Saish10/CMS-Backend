from django.db import models
from django.utils.translation import gettext_lazy as _
from DSR.utils import BaseModel, ULIDField
from colorfield.fields import ColorField


class Tenant(BaseModel):

    internal_id = ULIDField(_('tenant id'), editable=False)
    name = models.CharField(_('tenant name'), max_length=100)
    slug = models.SlugField(_('tenant slug'), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'

    @classmethod
    def get_tenant(cls, **criteria):
        return cls.objects.get(**criteria)

    @classmethod
    def filter_tenant(cls, **criteria):
        return cls.objects.filter(**criteria)


class TenantConfig(BaseModel):

    internal_id = ULIDField(_('tenant config id'), editable=False)
    logo = models.ImageField(_('logo'), editable=True, upload_to='DSR/static/logos')
    primary_color = ColorField(format="hexa", null=True)
    secondary_color = ColorField(format="hexa", null=True)
    tertiary_color = ColorField(format="hexa", null=True)
    tagline = models.TextField(_('tenant tagline'), null=True, db_index=True)
    url = models.URLField(_('tenant url'), unique=True, null=True)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        related_name='tenant_config'
    )

    def __str__(self):
        return f'Tenant Config: {self.id}'

    class Meta:
        unique_together = ('tenant',)
        verbose_name = 'Tenant Configurations'
        verbose_name_plural = 'Tenant Configurations'


    @classmethod
    def get_tenant_config(cls, **criteria):
        return cls.objects.get(**criteria)


# class TenantTheme(BaseModel):
#     internal_id = ULIDField(_('tenant theme id'), editable=False)

#     tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, related_name='tenant_theme')

#     def __str__(self):
#         return f'TenantTheme: {self.id}'

#     @classmethod
#     def get_tenant_theme(cls, **criteria):
#         return cls.objects.get(**criteria)