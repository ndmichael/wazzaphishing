from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmailUploadForm
from phishing.utils.ml_model import vectorizer, phishing_model, MODEL_PATH, VECTORIZER_PATH
from phishing.utils.process_email_file import extract_email_content
from phishing.utils.utils_phishing import extract_indicators, determine_risk_level
from django.core.exceptions import ValidationError
from .models import UploadedEmail, PhishingReport
import re
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Case, When, Value, IntegerField


@login_required
def scan_email(request):
    context = {"title": "scan email"}
    risk_level = flagged_words = urls = probability = None
    success = False

    if request.method == 'POST':
        form = EmailUploadForm(request.POST, request.FILES)

        if form.is_valid():
            email_instance = form.save(commit=False)
            email_instance.user = request.user

            try:
                data = extract_email_content(request.FILES['email_file'])
                email_instance.extracted_subject = data.get('subject')
                email_instance.extracted_sender = data.get('sender')
                email_instance.extracted_body = data.get('body', '')
                email_instance.save()
            except Exception as e:
                # Return JSON error for AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accepts('application/json'):
                    return JsonResponse({
                        'success': False,
                        'error': f"Failed to parse email file: {e}"
                    }, status=400)
                
                form.add_error('email_file', f"Failed to parse email file: {e}")
                context.update({"form": form})
                return render(request, "phishing/scan_email.html", context)

            # Predict & analyze
            risk_level, probability = determine_risk_level(
                phishing_model, vectorizer, email_instance.extracted_body
            )
            flagged_words, urls = extract_indicators(email_instance.extracted_body)

            # Save report
            PhishingReport.objects.create(
                email=email_instance,
                risk_level=risk_level,
                phishing_indicators={"flagged_words": flagged_words, "urls": urls},
            )

            success = True
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accepts('application/json'):
                return JsonResponse({
                    'success': True,
                    'risk_level': risk_level,
                    'flagged_words': flagged_words,
                    'urls': urls,
                    'probability': float(probability) if probability is not None else None
                })
        else:
            # Return JSON error for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accepts('application/json'):
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid form submission.',
                    'errors': form.errors
                }, status=400)
            
            messages.error(request, "Invalid form submission.")
    else:
        form = EmailUploadForm()

    context.update({
        "form": form,
        "success": success,
        "risk_level": risk_level,
        "flagged_words": flagged_words,
        "urls": urls,
        "probability": probability,
    })

    return render(request, "phishing/scan_email.html", context)

# @login_required
# def scan_email(request):
#     context = {"title": "scan email"}
#     risk_level = flagged_words = urls = probability = None
#     success = False

#     if request.method == 'POST':
#         form = EmailUploadForm(request.POST, request.FILES)

#         if form.is_valid():
#             email_instance = form.save(commit=False)
#             email_instance.user = request.user

#             try:
#                 data = extract_email_content(request.FILES['email_file'])
#                 email_instance.extracted_subject = data.get('subject')
#                 email_instance.extracted_sender = data.get('sender')
#                 email_instance.extracted_body = data.get('body', '')
#                 email_instance.save()
#             except Exception as e:
#                 form.add_error('email_file', f"Failed to parse email file: {e}")
#                 context.update({"form": form})
#                 return render(request, "phishing/scan_email.html", context)

#             # Predict & analyze
#             risk_level, probability = determine_risk_level(
#                 phishing_model, vectorizer, email_instance.extracted_body
#             )
#             flagged_words, urls = extract_indicators(email_instance.extracted_body)

#             # Save report
#             PhishingReport.objects.create(
#                 email=email_instance,
#                 risk_level=risk_level,
#                 phishing_indicators={"flagged_words": flagged_words, "urls": urls},
#             )

#             success = True
#             messages.success(request, "Email scanning completed successfully.")
#         else:
#             messages.error(request, "Invalid form submission.")
#     else:
#         form = EmailUploadForm()

#     context.update({
#         "form": form,
#         "success": success,
#         "risk_level": risk_level,
#         "flagged_words": flagged_words,
#         "urls": urls,
#         "probability": probability,
#     })

#     return render(request, "phishing/scan_email.html", context)


@login_required
def analysis_report(request):
    sort = request.GET.get("sort", "newest")  # default sort
    reports = PhishingReport.objects.filter(email__user=request.user)

    # Sorting logic
    if sort == "high":
        reports = reports.annotate(
            sort_order=Case(
                When(risk_level="High", then=Value(1)),
                When(risk_level="Medium", then=Value(2)),
                When(risk_level="Low", then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by("sort_order", "-created_at")

    elif sort == "low":
        reports = reports.annotate(
            sort_order=Case(
                When(risk_level="Low", then=Value(1)),
                When(risk_level="Medium", then=Value(2)),
                When(risk_level="High", then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by("sort_order", "-created_at")

    elif sort == "oldest":
        reports = reports.order_by("created_at")

    else:  # newest
        reports = reports.order_by("-created_at")

    paginator = Paginator(reports, 7)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "title": "analysis report",
        "page_obj": page_obj,
        "sort": sort,
    }

    return render(request, "phishing/analysis_report.html", context)


def user_settings(request):

    context = {
        "title": "settings",
    }
    return render(request, 'phishing/user_settings.html', context)