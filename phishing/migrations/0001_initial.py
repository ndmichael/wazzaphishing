# Generated by Django 5.1.2 on 2024-11-11 12:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_file', models.FileField(upload_to='emails/')),
                ('extracted_subject', models.CharField(blank=True, max_length=255, null=True)),
                ('extracted_sender', models.EmailField(blank=True, max_length=254, null=True)),
                ('extracted_body', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PhishingReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('risk_level', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=50)),
                ('phishing_indicators', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='phishing.uploadedemail')),
            ],
        ),
    ]
