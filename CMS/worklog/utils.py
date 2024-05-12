from datetime import datetime
from .models import TaskType, Project, DailyStatusReport
from CMS.utils import logger
from CMS.constants import ERROR_MSG


class DSRManager:

    def __init__(self, request):
        args = request.GET
        self.date = args.get('date')
        self.month = args.get(
            'month_year', f"{datetime.now().month}/{datetime.now().year}"
        )
        self.project = args.get('project')
        self.dsr_id = args.get('internal_id')

    def create(self, dsr_data, user):
        try:
            for data in dsr_data:
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
                _ = DailyStatusReport.objects.create(**dsr_data)
                # if not dsr:
                #     return False, "Failed to save Daily Status Report (DSR)."
            return True, "Daily Status Report (DSR) saved successfully."
        except Exception as e:
            logger.error(
                f'DailyStatusReport | Error in create :{e}', exc_info=True
            )
            return False, ERROR_MSG

    def get_daily_status_report(self, user):
        try:
            month, year = map(int, self.month.split('/'))
            queryset = (
                DailyStatusReport.objects.filter(
                    user=user, date__year=year, date__month=month
                ).all()
            )
            return self.filter(queryset)
            # return queryset
        except Exception as e:
            logger.error(
                f"DSRManager | Error in get_daily_status_report :{e}",
                exc_info=True
            )
            return None

    def filter(self, queryset):
        try:
            if self.date:
                queryset = queryset.filter(date=self.date)

            if self.project:
                queryset = queryset.filter(project__name=self.project)

            return queryset
        except Exception as e:
            logger.error(f'DSRManager | Error in filter :{e}', exc_info=True)
            return queryset

    def get_dsr_detail(self):
        try:
            detail = DailyStatusReport.objects.get(internal_id=self.dsr_id)
            return detail
        except Exception as e:
            logger.error(
                f'DSRManager | Error in get_dsr_detail :{e}', exc_info=True
            )
            return None

    def update(self, updates, user):
        try:

            dsr = DailyStatusReport.objects.get(internal_id=updates.get('internal_id'))
            task_type = TaskType.objects.get(slug=updates.get('task_type'))
            project = Project.objects.get(name=updates.get('project'))
            updates['user'] = user
            updates['task_type'] = task_type
            updates['project'] = project

            updated_fields = {}
            for field, value in updates.items():
                if hasattr(dsr, field) and getattr(dsr, field) != value:
                    setattr(dsr, field, value)
                    updated_fields[field] = value
                elif not hasattr(dsr, field):
                    logger.warning(f"DSRManager | Attribute {field} does not exist.")

            dsr.save()
            return (
                True, "DSR updated successfully." if updated_fields else True,
                "No fields were updated."
            )

        except Exception as e:
            logger.error(f"DSRManager | Error in update_dsr :{e}", exc_info=True)
            return None, ERROR_MSG
