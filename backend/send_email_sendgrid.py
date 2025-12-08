"""
SendGrid email sender - alternative to SMTP (Gmail)
Useful if you don't want to use Gmail or prefer SendGrid's service

Installation:
    pip install sendgrid

Setup:
    1. Create a SendGrid account at https://sendgrid.com
    2. Generate an API key: https://app.sendgrid.com/settings/api_keys
    3. Verify a sender email: https://app.sendgrid.com/settings/sender_auth
    4. Add to .env:
       SENDGRID_API_KEY=SG.xxx...xxx
       SENDGRID_FROM_EMAIL=your-verified@example.com
"""

import os
from dotenv import load_dotenv

load_dotenv()

def send_email_alert_sendgrid(to_email, subject, message):
    """Send email using SendGrid API instead of SMTP"""
    try:
        from sendgrid import SendGridAPIClient  # type: ignore
        from sendgrid.helpers.mail import Mail  # type: ignore
    except ImportError:
        raise Exception("SendGrid not installed. Run: pip install sendgrid")
    
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("SENDGRID_FROM_EMAIL")
    
    if not api_key or not from_email:
        raise Exception(
            "SendGrid not configured. Set SENDGRID_API_KEY and SENDGRID_FROM_EMAIL in .env"
        )
    
    try:
        mail = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=message
        )
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail)
        
        if response.status_code in [200, 201, 202]:
            print(f"Email sent successfully via SendGrid to {to_email}")
            return True
        else:
            raise Exception(f"SendGrid API error: {response.status_code}")
    except Exception as e:
        print(f"SendGrid email failed: {e}")
        raise Exception(f"Failed to send email via SendGrid: {str(e)}")


if __name__ == "__main__":
    # Test SendGrid
    try:
        send_email_alert_sendgrid(
            "test@example.com",
            "Test Email",
            "This is a test email from SendGrid"
        )
        print("SendGrid test successful!")
    except Exception as e:
        print(f"SendGrid test failed: {e}")
