import os
import email
from email import policy
from email.parser import BytesParser
import chardet

def extract_email_data(file_path):
    """
    Extracts the subject, sender, and body from an .eml or .txt file.

    Args:
        file_path (str): Path to the email file.

    Returns:
        dict: Dictionary containing 'subject', 'sender', and 'body'.
    """
    # Detect file encoding
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']

    # Parse the email content
    with open(file_path, 'r', encoding=encoding) as file:
        email_content = file.read()

    if file_path.endswith('.eml'):
        # Parse the .eml file
        msg = BytesParser(policy=policy.default).parsebytes(raw_data)
        subject = msg.get('Subject', 'No Subject')
        sender = msg.get('From', 'Unknown Sender')
        body = extract_email_body(msg)
    elif file_path.endswith('.txt'):
        # For .txt, assume structured content
        lines = email_content.splitlines()
        subject = next((line.split(':', 1)[1].strip() for line in lines if line.lower().startswith('subject:')), 'No Subject')
        sender = next((line.split(':', 1)[1].strip() for line in lines if line.lower().startswith('from:')), 'Unknown Sender')
        body = "\n".join(lines)
    else:
        raise ValueError("Unsupported file type. Only .eml or .txt files are allowed.")

    return {"subject": subject, "sender": sender, "body": body}

def extract_email_body(msg):
    """
    Extracts the body content from an email.message.EmailMessage object.

    Args:
        msg (email.message.EmailMessage): Parsed email message object.

    Returns:
        str: Body content of the email.
    """
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
    else:
        return msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')
    return "No Body"

# Example usage:
file_path = 'example_email.eml'  # Replace with your file path
email_data = extract_email_data(file_path)
print("Subject:", email_data['subject'])
print("Sender:", email_data['sender'])
print("Body:", email_data['body'])
