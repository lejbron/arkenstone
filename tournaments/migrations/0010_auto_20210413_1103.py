# Generated by Django 3.1.4 on 2021-04-13 11:03

import django.db.models.deletion

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournaments', '0009_match_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='tournament',
            field=models.ForeignKey(limit_choices_to={'tt_status__in': ['ann', 'reg', 'act']}, on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='tournaments.tournament'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='superviser',
            field=models.ForeignKey(help_text='Укажите организатора турнира', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_tournaments', to=settings.AUTH_USER_MODEL, verbose_name='Организатор'),
        ),
    ]
