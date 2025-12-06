from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('appointments/', views.appointments_view, name='appointments'),
    path('services/', views.services_view, name='services'),
    path('staff/', views.staff_view, name='staff'),
    path('customers/', views.customers_view, name='customers'),
]
