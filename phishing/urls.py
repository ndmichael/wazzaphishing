from django.contrib import admin
from django.urls import path
from .views import scan_email, analysis_report

urlpatterns = [
    path('scan/email/', scan_email, name="scan_email"),
    path('email/reports/', analysis_report, name="phishing_report"),
]