# Generated by Django 5.0.1 on 2024-04-07 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worklog', '0005_dailystatusreport_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailystatusreport',
            name='task_details',
        ),
        migrations.AddField(
            model_name='dailystatusreport',
            name='task',
            field=models.TextField(null=True, verbose_name='task'),
        ),
    ]
