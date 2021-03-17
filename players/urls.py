from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.player_detail_view, name='player-detail'),
]
