from django import forms
from .models import UploadedEmail

class EmailUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedEmail
        fields = ['email_file']