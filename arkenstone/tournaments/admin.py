from django.contrib import admin

from .models import PlayerStats, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'status', 'tours_amount',)


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player', 'game_points', 'tournament_points', 'difference',)
