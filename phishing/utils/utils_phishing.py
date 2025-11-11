# phishing/utils.py
import re
from phishing.models import PhishingReport

PHISHING_KEYWORDS = [
    "verify", "confirm", "update", "reset", "security alert", "unauthorized",
    "suspicious", "account locked", "urgent", "immediately", "asap",
    "within 24 hours", "your account will be closed", "last warning",
    "final notice", "important", "bank", "invoice", "payment", "refund",
    "billing", "statement", "wire transfer", "transaction", "amount",
    "click here", "login now", "open attachment", "act now", "take action",
    "respond", "sign in", "paypal", "apple", "google", "microsoft",
    "amazon", "netflix", "facebook", "irs", "support", "helpdesk",
    "you have won", "congratulations", "free", "gift", "limited offer",
    "reward", "claim", "lucky"
]

def extract_indicators(text):
    flagged_words = [
        word for word in PHISHING_KEYWORDS
        if re.search(rf"\b{word}\b", text, re.IGNORECASE)
    ]
    urls = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        text
    )
    return flagged_words, urls


def determine_risk_level(model, vectorizer, text):
    vectorized_text = vectorizer.transform([text])
    prediction = model.predict(vectorized_text)[0]
    probability = model.predict_proba(vectorized_text)[0][1]

    if int(prediction) == 1 and probability >= 0.8:
        level = PhishingReport.HIGH
    elif str(prediction) == '1' and probability >= 0.5:
        level = PhishingReport.MEDIUM
    else:
        level = PhishingReport.LOW

    return level, probability
