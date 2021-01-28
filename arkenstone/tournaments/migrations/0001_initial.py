# Generated by Django 3.1.4 on 2021-01-28 21:17

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('start_date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('ann', 'announce'), ('reg', 'registration'), ('creg', 'registration closed'), ('act', 'active'), ('fin', 'finished')], default='ann', max_length=4)),
                ('tours_amount', models.PositiveIntegerField(blank=True, default=3, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(6)])),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.PositiveIntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (6, 'Sixth')], default=1)),
                ('tour_status', models.CharField(choices=[('crt', 'created'), ('prd', 'paired'), ('act', 'active'), ('fin', 'finished'), ('arch', 'archived')], default='crt', max_length=4)),
                ('tournament', models.ForeignKey(limit_choices_to={'status__in': ['ann', 'reg', 'act']}, on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='tournaments.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('army', models.CharField(default='Shier', max_length=80)),
                ('game_points', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('tournament_points', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('difference', models.IntegerField(blank=True, default=0, null=True)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament')),
            ],
            options={
                'verbose_name_plural': 'Players Stats',
                'ordering': ['-tournament_points', '-difference', '-game_points'],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opp1_gp', models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(12)])),
                ('opp2_gp', models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(12)])),
                ('opp1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='opp1', to='tournaments.playerstats')),
                ('opp2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='opp2', to='tournaments.playerstats')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='tournaments.tour')),
            ],
            options={
                'verbose_name_plural': 'matches',
            },
        ),
        migrations.AddConstraint(
            model_name='tour',
            constraint=models.UniqueConstraint(fields=('order_num', 'tournament_id'), name='unique_tour'),
        ),
        migrations.AddConstraint(
            model_name='playerstats',
            constraint=models.UniqueConstraint(fields=('tournament', 'player'), name='unique_tournament_paleyr'),
        ),
    ]
