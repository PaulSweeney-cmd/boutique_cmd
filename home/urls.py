from django.contrib import admin
from django.urls import path
from . import views

# adding an empty path to indicate this is the route url
urlpatterns = [
    path('', views.index, name='home')
]
