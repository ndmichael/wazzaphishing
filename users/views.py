from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from phishing.models import PhishingReport


@login_required
def user_dashboard(request):
    total_phishing = PhishingReport.objects.all().count
    recent_reports  = PhishingReport.objects.filter(email__user=request.user).order_by("-created_at")[:4]

    # Count phishing reports by risk level
    risk_counts = PhishingReport.objects.values('risk_level').annotate(count=Count('risk_level'))
    risk_data = {item['risk_level']: item['count'] for item in risk_counts}

    context ={
        "title": "user dashboard",
        "total_phishing" :total_phishing,
        'risk_data': risk_data,
        'recent_reports': recent_reports
    }
    return render(request, "users/user_dashboard.html", context)

@login_required
def redirect_dashboard(request):
    return redirect('user_dashboard')
    # if request.user.is_staff:
    #     return redirect('admindashboard')
    