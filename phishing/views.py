from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmailUploadForm
from phishing.utils.ml_model import vectorizer, phishing_model
from phishing.utils.process_email_file import extract_email_content
from django.core.exceptions import ValidationError
import os
from django.conf import settings

@login_required
def scan_email(request):
    if request.method == 'POST':
        form = EmailUploadForm(request.POST, request.FILES)
        if form.is_valid():
            email_instance = form.save(commit=False)
            email_instance.user = request.user
            
            try:
                data = extract_email_content(request.FILES['email_file'])
                subject = data.get('subject')
                sender = data.get('sender')
                body = data.get('body')
                print(f"subject: {subject}, sender: {sender}, body: {body}")
                email_instance.extracted_subject = subject
                email_instance.extracted_sender = sender
                email_instance.extracted_body = body
                email_instance.save()
            except Exception as e:
                form.add_error('email_file', f"Failed to parse the email file: {e}")


            vectorized_text = vectorizer.transform(email_instance.extracted_body)

            return redirect('scan_email')  # Redirect to a success or report page
    else:
        form = EmailUploadForm()

    context ={
        "title": "user dashboard",
        "form": form
    }
    return render(request, "phishing/scan_email.html", context)
