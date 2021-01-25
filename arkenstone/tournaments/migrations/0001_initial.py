# Generated by Django 3.1.4 on 2021-01-25 17:12

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
                ('title', models.CharField(max_length=200)),
                ('start_date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('ann', 'announce'), ('reg', 'registration'), ('creg', 'registration closed'), ('act', 'active'), ('fin', 'finished')], default='ann', max_length=4)),
                ('tours_amount', models.PositiveIntegerField(blank=True, default=3, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(6)])),
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
        ),
    ]
