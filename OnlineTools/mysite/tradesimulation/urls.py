# tradesimulation/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.trade_simulation, name='trade_simulation'),
    path('process_form/', views.process_form, name='process_form'),
    # Define your URL patterns for the app here
]
