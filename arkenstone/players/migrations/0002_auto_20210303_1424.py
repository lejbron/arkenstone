# Generated by Django 3.1.4 on 2021-03-03 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tournaments', '0001_initial'),
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament'),
        ),
        migrations.AddConstraint(
            model_name='playerstats',
            constraint=models.UniqueConstraint(fields=('tournament', 'player'), name='unique_tournament_player'),
        ),
    ]
