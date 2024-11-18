import os
import email
from email import message_from_string, message_from_bytes
from django.core.files.storage import default_storage

# from email.parser import BytesParser
# import chardet
def extract_email_content(uploaded_file):
    # Read the file in memory
    file_content = uploaded_file.read().decode("utf-8", errors="ignore")  # Decode for .txt or .eml
    
    # Determine file type based on extension
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    # print(f"file content: {file_content}")
    # print(f"file content: {file_extension}")

    if file_extension == '.eml':
        # Parse the .eml file
        # Parse as .eml file
        email_message = message_from_string(file_content)
        subject = email_message.get("Subject", "").strip()
        sender = email_message.get("From", "").strip()
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                    break
        else:
            body = email_message.get_payload(decode=True).decode(email_message.get_content_charset() or "utf-8")

        # print("Email data: " + sender)
        # print("Email subject: " + subject)
        # print("Email body: " + body)

    elif file_extension == ".txt":
        # Parse as .txt file (simple extraction example)
        lines = file_content.splitlines()
        for line in lines:
            if line.lower().startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
            elif line.lower().startswith("from:"):
                sender = line.split(":", 1)[1].strip()
            else:
                body += line + "\n"  # Treat the rest as body text
    else:
        raise ValueError("Unsupported file type. Only .eml or .txt files are allowed.")


    # Only save the file if the body or file content is non-empty
    if body.strip():
        save_path = os.path.join("emails", uploaded_file.name)
        default_storage.save(save_path, uploaded_file)
        return {
            "subject": subject,
            "sender": sender,
            "body": body.strip(),
            "file_saved": True,
            "saved_path": save_path,
        }
    
    return {
        "subject": subject,
        "sender": sender,
        "body": body.strip(),
        "file_saved": False,
    }
