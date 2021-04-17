from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('homepage.urls')),
]

urlpatterns += [
    path('auth/', include('asgard.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('players/', include('players.urls')),
]

urlpatterns += [
    path('tournaments/', include('tournaments.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
