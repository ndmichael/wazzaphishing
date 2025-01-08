from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from phishing.models import PhishingReport


@login_required
def user_dashboard(request):
    total_phishing = PhishingReport.objects.all().count
    context ={
        "title": "user dashboard",
        "total_phishing" :total_phishing
    }
    return render(request, "users/user_dashboard.html", context)

@login_required
def redirect_dashboard(request):
    return redirect('user_dashboard')
    # if request.user.is_staff:
    #     return redirect('admindashboard')
    