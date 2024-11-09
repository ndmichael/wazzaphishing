from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmailUploadForm


@login_required
def scan_email(request):
    if request.method == 'POST':
        form = EmailUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            # You can now parse the uploaded file for phishing analysis
            return redirect('success_page')  # Redirect to a success or report page
    else:
        form = EmailUploadForm()

    context ={
        "title": "user dashboard",
        "form": form
    }
    return render(request, "phishing/scan_email.html", context)
