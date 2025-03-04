# Generated by Django 3.1.4 on 2021-03-03 14:24

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('players', '0001_initial'),
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
                ('tt_slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.PositiveIntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (6, 'Sixth')], default=1)),
                ('tour_status', models.CharField(choices=[('crt', 'created'), ('prd', 'paired'), ('act', 'active'), ('fin', 'finished'), ('arch', 'archived')], default='crt', max_length=4)),
                ('tour_results', models.JSONField(blank=True, null=True)),
                ('tour_slug', models.SlugField(null=True, unique=True)),
                ('tournament', models.ForeignKey(limit_choices_to={'status__in': ['ann', 'reg', 'act']}, on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='tournaments.tournament')),
            ],
            options={
                'ordering': ['tournament', 'order_num'],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opp1_gp', models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(12)])),
                ('opp2_gp', models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(12)])),
                ('match_slug', models.SlugField(null=True, unique=True)),
                ('opp1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='opp1', to='players.playerstats')),
                ('opp2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='opp2', to='players.playerstats')),
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
    ]
