from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('booking/', views.booking, name='booking'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('process_payment/', views.process_payment, name='process_payment'),


    path('manage_all/', views.manage_all_view, name='manage_all'),  # Management page


    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
