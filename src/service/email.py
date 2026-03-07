import os
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# The server runs from /src, so we need to go up one level to find the .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT", "587")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_verification_email(to_email: str, token: str, is_mock: bool = True):
    """
    Sends an email with a verification link.
    If is_mock is True, it will just print the email to the console.
    """
    verification_link = f"http://localhost:8000/verify-email?token={token}"
    
    # We will also provide a frontend link if you prefer the user to land on the frontend
    # but for simplicity, we'll verify directly via a GET request to the backend first.
    # frontend_link = f"http://localhost:5173/verify?token={token}"

    subject = "Verify your email address for Usha Toys"
    body = f"""
    Hello!
    
    Welcome to Usha Toys! Please verify your email address to complete your registration.
    
    Click the link below to verify:
    {verification_link}
    
    If you did not create an account, you can safely ignore this email.
    """

    if is_mock or not SMTP_HOST or not SMTP_USER:
        print("="*50)
        print("MOCK EMAIL SENT (No SMTP configured or is_mock=True)")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(body)
        print("="*50)
        return True

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_HOST, int(SMTP_PORT))
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Verification email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False
