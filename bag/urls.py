from django.urls import path
from . import views

# adding an empty path to indicate this is the route url
urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>', views.add_to_bag, name='add_to_bag')
]
