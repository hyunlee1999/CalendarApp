# Generated by Django 3.1.6 on 2021-03-26 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarApp', '0008_auto_20210325_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='importanceLevel',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)], default=0),
        ),
    ]
