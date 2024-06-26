from CMS.utils import BaseModel, ULIDField, logger
from django.db import models
from django.utils.translation import gettext_lazy as _
from CMS.constants import ERROR_MSG
from tenant.models import Tenant


class Project(BaseModel):

    internal_id = ULIDField(_('project ulid'), editable=False)
    name = models.CharField(_('project name'), max_length=100)
    description = models.TextField()
    assigned_users = models.ManyToManyField(
        'user.UserAccount',
        verbose_name=_('assigned users'),
        related_name='assigned_projects',
        blank=True,
    )
    tenant = models.ForeignKey(
        'tenant.Tenant',
        on_delete=models.CASCADE,
        null=True,
        )

    def __str__(self):
        return self.name

    @classmethod
    def filter_project(cls, **criteria):
        return cls.objects.filter(**criteria)

    def get_project_list(self, tenant):
        return self.filter_project(tenant=tenant).all()


class TaskType(BaseModel):

    internal_id = ULIDField(_('task type ulid'), editable=False)
    name = models.CharField(_('type'), max_length=150)
    slug = models.SlugField(_('type slug'), max_length=150)

    def __str__(self):
        return self.name

    @classmethod
    def filter_task_type(cls, **criteria):
        return cls.objects.filter(**criteria)

    def get_task_type_list(self):
        return self.filter_task_type(is_active=True).all()


class DailyStatusReport(BaseModel):

    internal_id = ULIDField(_('dsr ulid'), editable=False)
    date = models.DateField(_('date'))
    task = models.TextField(_('task'), null=True)
    status_summary = models.TextField(_('status summary'))
    hours_worked = models.DecimalField(_('hours worked'), max_digits=5, decimal_places=2)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey('user.UserAccount', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.full_name} - {self.date}"


