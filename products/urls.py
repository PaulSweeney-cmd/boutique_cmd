from django.urls import path
from . import views

# adding an empty path to indicate this is the route url
urlpatterns = [
    path('', views.all_products, name='products')
]
