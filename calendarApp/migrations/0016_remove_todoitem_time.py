# Generated by Django 3.1.6 on 2021-04-08 01:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendarApp', '0015_todoitem_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todoitem',
            name='time',
        ),
    ]