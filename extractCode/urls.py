from django.contrib import admin
from .views import netflix_otp_extractor
from django.urls import path

urlpatterns = [
   
    path('netflix-otp/', netflix_otp_extractor, name='netflix_otp'),
]
