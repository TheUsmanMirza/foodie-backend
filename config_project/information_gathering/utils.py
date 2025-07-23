import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config_project.config import settings
from restaurants import repository


def send_email(receiver_email: str, subject: str, message: str):
    """
    Send an email using SMTP
    
    Args:
        receiver_email (str): Email address of the recipient
        subject (str): Subject of the email
        message (str): HTML content of the email
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = settings.SMTP_EMAIL
    msg['To'] = receiver_email

    # Attach the HTML message
    msg.attach(MIMEText(message, 'html'))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise
