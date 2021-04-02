# Generated by Django 3.1.4 on 2021-04-02 15:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_auto_20210402_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='start_time',
            field=models.TimeField(default=datetime.time(15, 21, 25, 534837)),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2021, 4, 2, 15, 21, 25, 534807), null=True),
        ),
    ]
