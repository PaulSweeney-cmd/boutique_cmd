from django.urls import path
from . import views

# adding an empty path to indicate this is the route url
urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]