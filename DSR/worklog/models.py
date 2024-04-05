from DSR.utils import BaseModel, ULIDField, logger
from django.db import models
from django.utils.translation import gettext_lazy as _
from DSR.constants import ERROR_MSG
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


class DailyStatusReport(models.Model):

    internal_id = ULIDField(_('dsr ulid'), editable=False)
    date = models.DateField(_('date'))
    task_details = models.TextField(_('task details'))
    status_summary = models.TextField(_('status summary'))
    hours_worked = models.DecimalField(_('hours worked'), max_digits=5, decimal_places=2)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey('user.UserAccount', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.full_name} - {self.date}"

    @classmethod
    def create(cls, data, user):
        try:
            date = data.get('date')
            task_details = data.get('task_details')
            status_summary = data.get('status_summary')
            hours_worked = data.get('hours_worked')
            task_type = data.get('task_type')
            project = data.get('project')

            task_type = TaskType.objects.get_or_create(slug=task_type)
            project = Project.objects.get(name=project)

            dsr_data = {
                "date": date,
                "task_details": task_details,
                "status_summary": status_summary,
                "hours_worked": hours_worked,
                "task_type": task_type,
                "project":project,
                "user": user
            }
            dsr = cls.objects.create(**dsr_data)
            if not dsr:
                return False, "Failed to save Daily Status Report (DSR)."
            return True, "Daily Status Report (DSR) saved successfully."
        except Exception as e:
            logger.error(
                f'DailyStatusReport | Error in create :{e}', exc_info=True)
            return False, ERROR_MSG