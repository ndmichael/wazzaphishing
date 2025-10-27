from django.shortcuts import render


def index(request):
    context = {
        'title': 'Ruqayya anti - phishing software'
    }
    return render(request, "pages/index.html", context)
