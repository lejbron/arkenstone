# Generated by Django 3.1.4 on 2021-04-15 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0011_auto_20210415_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='tournament',
            field=models.ForeignKey(blank=True, limit_choices_to={'tt_status__in': ['ann', 'reg', 'act']}, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament'),
        ),
    ]
