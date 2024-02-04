# Generated by Django 5.0.1 on 2024-02-04 06:46

import DSR.utils
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(blank=True, max_length=500)),
                ('updated_by', models.CharField(blank=True, max_length=500)),
                ('internal_id', DSR.utils.ULIDField(editable=False, max_length=26, verbose_name='project ulid')),
                ('name', models.CharField(max_length=100, verbose_name='project name')),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(blank=True, max_length=500)),
                ('updated_by', models.CharField(blank=True, max_length=500)),
                ('internal_id', DSR.utils.ULIDField(editable=False, max_length=26, verbose_name='task type ulid')),
                ('name', models.CharField(max_length=150, verbose_name='type')),
                ('slug', models.SlugField(max_length=150, verbose_name='type slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DailyStatusReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_id', DSR.utils.ULIDField(editable=False, max_length=26, verbose_name='dsr ulid')),
                ('date', models.DateField(verbose_name='date')),
                ('task_details', models.TextField(verbose_name='task details')),
                ('status_summary', models.TextField(verbose_name='status summary')),
                ('hours_worked', models.DecimalField(decimal_places=2, editable=False, max_digits=5, verbose_name='hours worked')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worklog.project')),
                ('task_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='worklog.tasktype')),
            ],
        ),
    ]
