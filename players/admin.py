from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import PlayerStats, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class PlayerAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_bdate')
    list_select_related = ('profile', )

    def get_bdate(self, instance):
        return instance.profile.birth_date
    get_bdate.short_description = 'Birthday Date'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(PlayerAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, PlayerAdmin)


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'tournament', 'army', 'game_points', 'tournament_points', 'difference',)
