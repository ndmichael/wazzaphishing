from django.contrib import admin
from .models import UploadedEmail, PhishingReport

admin.site.register(UploadedEmail)
admin.site.register(PhishingReport)
