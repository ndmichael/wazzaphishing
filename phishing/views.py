from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmailUploadForm
from phishing.utils.process_email_file import extract_email_content
from django.core.exceptions import ValidationError

@login_required
def scan_email(request):
    if request.method == 'POST':
        form = EmailUploadForm(request.POST, request.FILES)
        if form.is_valid():
            email_instance = form.save(commit=False)
            email_instance.user = request.user
            
            # Extract email details
            # and save model
            try:
                extract_email_content(email_instance, request.FILES['email_file'])
                email_instance.save()
            except Exception as e:
                 form.add_error('email_file', f"Failed to parse the email file: {e}")

            return redirect('scan_email')  # Redirect to a success or report page
    else:
        form = EmailUploadForm()

    context ={
        "title": "user dashboard",
        "form": form
    }
    return render(request, "phishing/scan_email.html", context)
