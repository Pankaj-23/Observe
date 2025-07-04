import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ✅ Load the .env file from absolute path
dotenv_path = "/home/ansiblestart/Observe/AnsibleServicenow/.env"
print(f"[DEBUG] Loading .env from: {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)

# ✅ Read environment variables
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ✅ Debug log
print(f"[DEBUG] EMAIL_HOST: {EMAIL_HOST}")
print(f"[DEBUG] EMAIL_PORT: {EMAIL_PORT}")
print(f"[DEBUG] EMAIL_USER: {EMAIL_USER}")
print(f"[DEBUG] EMAIL_PASS: {'*' * len(EMAIL_PASS) if EMAIL_PASS else 'Not Set'}")
print(f"[DEBUG] EMAIL_RECEIVER: {EMAIL_RECEIVER}")

# ✅ Compose and send email
try:
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = "Test Alert: ServiceNow Closed Incidents"
    body = "This is a test alert to verify the email configuration."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
    server.quit()

    print("[SUCCESS] Email sent successfully.")
except Exception as e:
    print(f"[ERROR] Failed to send email: {e}")
