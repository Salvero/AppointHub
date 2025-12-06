from django.urls import path

from . import views

app_name = 'shops'

urlpatterns = [
    path('setup/', views.shop_setup_view, name='setup'),
    path('<slug:slug>/', views.shop_public_view, name='public'),
    path('<slug:slug>/dashboard/', views.shop_dashboard_view, name='dashboard'),
    path('<slug:slug>/edit/', views.shop_edit_view, name='edit'),
    path('<slug:slug>/hours/', views.shop_hours_view, name='hours'),
    path('<slug:slug>/closures/', views.shop_closures_view, name='closures'),
    path('<slug:slug>/closures/<int:pk>/delete/', views.shop_closure_delete_view, name='closure_delete'),
]
