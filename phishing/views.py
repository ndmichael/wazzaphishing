from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def scan_email(request):
    context ={
        "title": "user dashboard"
    }
    return render(request, "phishing/scan_email.html", context)
