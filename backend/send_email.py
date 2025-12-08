import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_email_alert(to_email, subject, message):
    """Send email alert to user.
    
    Supports two methods:
    1. Gmail SMTP (via .env SMTP_* variables)
    2. SendGrid API (via .env SENDGRID_API_KEY and SENDGRID_FROM_EMAIL)
    
    Falls back to SendGrid if SMTP is not configured.
    """
    SMTP_USER = os.getenv("SMTP_USER", "your_email@gmail.com")
    
    # Try SMTP first if configured
    if SMTP_USER != "your_email@gmail.com":
        try:
            return _send_via_smtp(to_email, subject, message)
        except Exception as smtp_error:
            # Fall back to SendGrid if available
            if os.getenv("SENDGRID_API_KEY"):
                print(f"[Email] SMTP failed, falling back to SendGrid: {smtp_error}")
                return _send_via_sendgrid(to_email, subject, message)
            else:
                raise
    else:
        # SMTP not configured, try SendGrid
        return _send_via_sendgrid(to_email, subject, message)


def _send_via_smtp(to_email, subject, message):
    """Send via Gmail SMTP"""
    SMTP_USER = os.getenv("SMTP_USER", "your_email@gmail.com")
    SMTP_PASS = os.getenv("SMTP_PASS", "your_app_password")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
    
    if SMTP_USER == "your_email@gmail.com":
        msg = (
            "SMTP not configured. Create a .env file in backend/ with SMTP_USER and SMTP_PASS "
            "(Gmail: generate an App Password). See EMAIL_SETUP.md for details."
        )
        print(msg)
        raise Exception(msg)
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(msg['From'], [to_email], msg.as_string())
        print(f"Email sent successfully via SMTP to {to_email}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        error_msg = (
            "SMTP authentication failed. Check SMTP_USER and SMTP_PASS (App Password for Gmail), "
            "ensure 2FA is enabled and the app password is correct. Original error: " + str(e)
        )
        print(f"Email auth failed: {e}")
        raise Exception(error_msg)
    except Exception as e:
        print(f"Email failed: {e}")
        raise Exception(f"Failed to send email: {str(e)}")


def _send_via_sendgrid(to_email, subject, message):
    """Send via SendGrid API"""
    try:
        from sendgrid import SendGridAPIClient  # type: ignore
        from sendgrid.helpers.mail import Mail  # type: ignore
    except ImportError:
        raise Exception(
            "SendGrid not installed. Run: pip install sendgrid, or configure Gmail SMTP"
        )
    
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("SENDGRID_FROM_EMAIL")
    
    if not api_key or not from_email:
        raise Exception(
            "SendGrid not configured. Set SENDGRID_API_KEY and SENDGRID_FROM_EMAIL in .env, "
            "or configure Gmail SMTP. See EMAIL_SETUP.md for details."
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

