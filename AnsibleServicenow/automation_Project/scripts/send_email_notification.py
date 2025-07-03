import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv()

print("[DEBUG] EMAIL_HOST:", os.getenv("EMAIL_HOST"))
print("[DEBUG] EMAIL_PORT:", os.getenv("EMAIL_PORT"))
print("[DEBUG] EMAIL_USER:", os.getenv("EMAIL_USER"))
print("[DEBUG] EMAIL_PASS:", os.getenv("EMAIL_PASS")[:4] + "****")  # hide full password
print("[DEBUG] EMAIL_RECEIVER:", os.getenv("EMAIL_RECEIVER"))

# Environment variables
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def send_email_notification(subject, body):
    if not all([EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVER]):
        raise Exception("Missing one or more required email environment variables.")

    # Compose email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
            print(f"[EMAIL SENT] Notification sent to {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {str(e)}")


if __name__ == "__main__":
    send_email_notification(
        subject="Incident Auto-Closure Report",
        body="All resolved ServiceNow incidents have been automatically closed.",
    )
