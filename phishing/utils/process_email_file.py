import os
import mailparser
from django.core.files.storage import default_storage

def extract_email_content(uploaded_file):
    # Read the file in memory
    file_content_bytes = uploaded_file.read()  # Read as bytes

    # Determine file type based on extension
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    subject = ""
    sender = ""
    body = ""

    if file_extension == '.eml':
        # Use mailparser for robust .eml parsing
        mail = mailparser.parse_from_bytes(file_content_bytes)

        subject = mail.subject or ""
        sender = mail.from_[0][1] if mail.from_ else ""
        body = "\n".join(mail.text_plain or []) or mail.body or ""

    elif file_extension == ".txt":
        # Parse as plain .txt (basic fallback logic)
        file_content = file_content_bytes.decode("utf-8", errors="ignore")
        lines = file_content.splitlines()
        collecting_body = False
        for line in lines:
            if line.lower().startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
            elif line.lower().startswith("from:"):
                sender = line.split(":", 1)[1].strip()
            else:
                if collecting_body or line.strip():  # Start collecting once headers end
                    collecting_body = True
                    body += line + "\n"

    else:
        raise ValueError("Unsupported file type. Only .eml or .txt files are allowed.")

    # Save the file if we extracted body content
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
