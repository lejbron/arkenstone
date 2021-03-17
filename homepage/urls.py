from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users_list_view, name='users-list'),
]
