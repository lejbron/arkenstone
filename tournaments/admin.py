from django.contrib import admin

from .models import Match, Tour, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'start_date', 'tours_amount',
        'tt_status', 'tt_category', 'tt_type')
    list_filter = (
        'tt_status', 'tt_category', 'tt_type'
    )
    fieldsets = (
      ('Tournament info', {
          'fields': ('title', 'start_date', 'tours_amount')
      }),
      ('Management', {
          'fields': ('tt_category', 'tt_type')
      }),
      ('Administration', {
          'fields': ('tt_status', 'tt_slug')
      }),
    )


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('order_num', 'tour_status', 'tournament',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tour', 'opp1', 'opp2', 'opp1_gp', 'opp2_gp')
