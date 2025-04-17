from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_page, name='register_page'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify/', views.verify_and_save, name='verify'),
]