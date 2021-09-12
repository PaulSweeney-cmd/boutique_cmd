from django.urls import path
from . import views

# adding an empty path to indicate this is the route url
urlpatterns = [
    path('', views.checkout, name='checkout'),
    # Stripe
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success')
]
