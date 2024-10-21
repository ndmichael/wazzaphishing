from django.shortcuts import render


def index(request):
    context = {
        'title': 'Wazza anti - phishing software'
    }
    return render(request, "pages/index.html", context)
