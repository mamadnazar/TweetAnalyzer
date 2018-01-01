from django.urls import path

from . import views

urlpatterns = [
    path('update', views.updateDB, name = 'update-db'),
    path('', views.index, name = 'index'),
]