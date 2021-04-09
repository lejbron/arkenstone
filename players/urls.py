from django.urls import path

from . import views

urlpatterns = [
    path('<int:player_id>/', views.player_detail_view, name='player-detail'),
]
