from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import CustomUser



class UploadedEmail(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email_file = models.FileField(upload_to='emails/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Uploaded Email by {self.user.username} at {self.uploaded_at}"

class PhishingReport(models.Model):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    
    RISK_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    email = models.ForeignKey(UploadedEmail, on_delete=models.CASCADE, related_name='reports')
    risk_level = models.CharField(max_length=50, choices=RISK_CHOICES)
    phishing_indicators = models.JSONField()  # Store structured phishing indicators (URLs, words, etc.)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.email.subject} - Risk: {self.risk_level}"

    def summary_of_indicators(self):
        """Returns a human-readable summary of the phishing indicators."""
        flagged_words = ', '.join(self.phishing_indicators.get('flagged_words', []))
        flagged_urls = ', '.join(self.phishing_indicators.get('urls', []))
        return f"Flagged Words: {flagged_words}, Flagged URLs: {flagged_urls}"

    def calculate_risk_score(self):
        """Calculate a custom risk score based on indicators."""
        words_risk = len(self.phishing_indicators.get('flagged_words', [])) * 0.4
        urls_risk = len(self.phishing_indicators.get('urls', [])) * 0.6
        return min(words_risk + urls_risk, 1.0)  # Normalize to a max score of 1.0

