# Generated by Django 3.1.6 on 2021-03-10 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarApp', '0003_todoitem_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='deadline',
            field=models.DateField(blank=True),
        ),
    ]