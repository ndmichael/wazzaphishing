import mailparser
import os
from django.conf import settings

def extract_email_content(email_instance, uploaded_file):
    # email_file_path = os.path.join(settings.MEDIA_ROOT, email_instance.email_file.path)
    # parsed_email = mailparser.parse_from_file(email_file_path)
    parsed_email = mailparser.parse_from_string(uploaded_file.read().decode('utf-8', errors='ignore'))
    
    # Extract relevant data
    email_instance.extracted_subject = parsed_email.subject
    email_instance.extracted_sender = parsed_email.from_[0][1]  # Extract sender email
    email_instance.extracted_body = parsed_email.body
    
    # Save the parsed data
    email_instance.save()
