from django.contrib import admin
from django.urls import path
from .views import scan_email

urlpatterns = [
    path('scan/email/', scan_email, name="scan_email"),
]