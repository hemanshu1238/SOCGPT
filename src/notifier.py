"""
notifier.py - Email / Slack integration for sending SOC analysis reports.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import yaml


def _load_config() -> dict:
    """Load email configuration from settings.yaml."""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def send_email_report(subject: str, report: str, email_to: str) -> None:
    """
    Sends an analysis report via email using SMTP (Gmail by default).

    Args:
        subject: Email subject line.
        report: The report body text.
        email_to: Recipient email address.
    """
    config = _load_config()
    sender_email = config.get("sender_email", "")
    email_password = config.get("email_password", "")

    if not sender_email or not email_password:
        print(f"[SOCGPT] Email not configured. Printing report to console instead.")
        print(f"=" * 60)
        print(f"TO: {email_to}")
        print(f"SUBJECT: {subject}")
        print(report)
        print(f"=" * 60)
        return

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.attach(MIMEText(report, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, email_to, msg.as_string())
        print(f"[SOCGPT] Report sent to {email_to}")
    except Exception as e:
        print(f"[SOCGPT] Failed to send email: {e}")
        print(f"[SOCGPT] Printing report to console instead.")
        print(f"=" * 60)
        print(f"TO: {email_to}")
        print(f"SUBJECT: {subject}")
        print(report)
        print(f"=" * 60)
