from django.urls import path
from . import views

urlpatterns = [
  path('', views.get_routes, name='home'),
  path('map', views.get_map, name='map')
]