from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmailUploadForm
from phishing.utils.ml_model import vectorizer, phishing_model, MODEL_PATH, VECTORIZER_PATH
from phishing.utils.process_email_file import extract_email_content
from django.core.exceptions import ValidationError
from .models import UploadedEmail, PhishingReport
import re
from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required
def scan_email(request):
    if request.method == 'POST':
        form = EmailUploadForm(request.POST, request.FILES)
        if form.is_valid():
            email_instance = form.save(commit=False)
            email_instance.user = request.user
            
            try:
                data = extract_email_content(request.FILES['email_file'])
                # print(f"data: {data}")
                subject = data.get('subject')
                sender = data.get('sender')
                body = data.get('body')

                email_instance.extracted_subject = subject
                email_instance.extracted_sender = sender
                email_instance.extracted_body = body
                email_instance.save()
            except Exception as e:
                form.add_error('email_file', f"Failed to parse the email file: {e}")
            
            encoded_label = {'phishing': 1, 'legitimate': 0}
            vectorized_text = vectorizer.transform([email_instance.extracted_body])
            # # Step 3: Predict risk level using the ML model
            risk_prediction = phishing_model.predict(vectorized_text)[0]
            probability = phishing_model.predict_proba(vectorized_text)[0][1]  
        
            # Step 4: Map the prediction to risk levels
            if int(risk_prediction) == 1 and probability >= 0.8:
                risk_level = PhishingReport.HIGH 
            elif str(risk_prediction) == '1' and probability >= 0.5:
                risk_level = PhishingReport.MEDIUM
            else:
                risk_level = PhishingReport.LOW
            

            # Step 5: Extract phishing indicators
            phishing_keywords = ["urgent", "click", "verify", "account", "login"]
            flagged_words = [word for word in phishing_keywords if word in email_instance.extracted_body]
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_instance.extracted_body)

            # Step 6: Create a phishing report
            phishing_indicators = {
                "flagged_words": flagged_words,
                "urls": urls
            }
            phishing_report = PhishingReport(
                email=email_instance,
                risk_level=risk_level,
                phishing_indicators=phishing_indicators,
            )
            phishing_report.save()
            print(f"risk prediction: {risk_prediction}")
            # Return JSON response
            return JsonResponse({
                'success': True,
                'risk_level': risk_level,
                'flagged_words': flagged_words,
                'urls': urls,
                "risk_percent": probability,
            })
        
            

            # return redirect('scan_email')  # Redirect to a success or report page
    else:
        form = EmailUploadForm()

    context ={
        "title": "user dashboard",
        "form": form
    }
    return render(request, "phishing/scan_email.html", context)
