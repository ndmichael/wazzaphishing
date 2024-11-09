from django import forms
from .models import UploadedEmail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Row, BaseInput
from crispy_bootstrap5.bootstrap5 import FloatingField, Field

class EmailUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedEmail
        fields = ['email_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field("email_file", wrapper_class='col-md-12', accept=".txt,.eml"),
            )
        )