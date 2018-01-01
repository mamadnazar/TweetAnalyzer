from django.urls import path

from . import views

urlpatterns = [
    path('update', views.index, name = 'index'),
    path('', views.index, name = 'index'),
]