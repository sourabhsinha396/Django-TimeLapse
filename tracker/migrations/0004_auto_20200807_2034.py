# Generated by Django 3.1 on 2020-08-07 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20200807_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktracker',
            name='date',
        ),
        migrations.AlterField(
            model_name='tasktracker',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tasktracker',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
