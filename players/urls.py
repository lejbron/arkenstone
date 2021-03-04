from django.urls import path

from . import views

urlpatterns = [
    path('', views.players_list_view, name='players-list'),
    path('<int:pk>/', views.player_detail_view, name='player-detail'),
]
