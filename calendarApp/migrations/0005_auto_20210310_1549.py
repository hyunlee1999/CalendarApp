# Generated by Django 3.1.6 on 2021-03-10 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarApp', '0004_auto_20210310_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]