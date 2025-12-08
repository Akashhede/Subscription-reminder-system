from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.database import SessionLocal
from backend.schemas import UserCreate, UserOut, UserUpdate, TestEmailRequest
from backend.models import User
from backend import crud, auth
from backend.send_email import send_email_alert
from jose import jwt
from jose import JWTError, ExpiredSignatureError
import os
import smtplib
import hashlib
from backend import auth as auth_module

router = APIRouter()

# Shared JWT secret from environment
SECRET_KEY = os.getenv("SECRET_KEY", "change_me_to_a_random_secret")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(authorization: str = Header(None)):
    """Extract user ID from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")
    parts = authorization.split()
    if len(parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = parts[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return int(payload.get("user_id"))
    except ExpiredSignatureError:
        # Token expired
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        # General JWT decode/validation error
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing = crud.get_user_by_email(db, user.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        try:
            created = crud.create_user(db, user.email, user.password, user.phone)
            return created
        except IntegrityError as e:
            db.rollback()
            if "UNIQUE constraint failed" in str(e):
                raise HTTPException(status_code=400, detail="Email already registered")
            raise HTTPException(status_code=400, detail="Registration failed")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

@router.post("/login")
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "phone": user.phone, "email_alerts_enabled": user.email_alerts_enabled}}

@router.get("/profile", response_model=UserOut)
def get_profile(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Get current user profile"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/profile", response_model=UserOut)
def update_profile(update_data: UserUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Update user profile preferences"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if update_data.email_alerts_enabled is not None:
        user.email_alerts_enabled = update_data.email_alerts_enabled
    if update_data.phone is not None:
        user.phone = update_data.phone
    
    db.commit()
    db.refresh(user)
    return user

@router.post("/send-test-email")
def send_test_email(request: TestEmailRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Send a test email to verify email configuration"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    subject = request.subject or "Test Email from Subscription Reminder"
    message = request.message or "This is a test email."
    
    if not user.email_alerts_enabled:
        raise HTTPException(status_code=400, detail="Email alerts are disabled. Please enable them first.")
    
    try:
        send_email_alert(user.email, subject, message)
        return {"status": "success", "message": f"Test email sent successfully to {user.email}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send test email: {str(e)}")


@router.post("/smtp-config")
def update_smtp_config(
    smtp_user: str,
    smtp_pass: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update SMTP configuration in .env file (admin-only in production)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # For now, allow any authenticated user to update (restrict to admin role in production)
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    
    try:
        # Read current .env
        env_content = ""
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                env_content = f.read()
        
        # Update values
        lines = env_content.split("\n")
        updated_lines = []
        found_keys = set()
        
        for line in lines:
            if line.startswith("SMTP_USER="):
                updated_lines.append(f"SMTP_USER={smtp_user}")
                found_keys.add("SMTP_USER")
            elif line.startswith("SMTP_PASS="):
                updated_lines.append(f"SMTP_PASS={smtp_pass}")
                found_keys.add("SMTP_PASS")
            elif line.startswith("SMTP_SERVER="):
                updated_lines.append(f"SMTP_SERVER={smtp_server}")
                found_keys.add("SMTP_SERVER")
            elif line.startswith("SMTP_PORT="):
                updated_lines.append(f"SMTP_PORT={smtp_port}")
                found_keys.add("SMTP_PORT")
            else:
                updated_lines.append(line)
        
        # Add missing keys
        if "SMTP_USER" not in found_keys:
            updated_lines.append(f"SMTP_USER={smtp_user}")
        if "SMTP_PASS" not in found_keys:
            updated_lines.append(f"SMTP_PASS={smtp_pass}")
        if "SMTP_SERVER" not in found_keys:
            updated_lines.append(f"SMTP_SERVER={smtp_server}")
        if "SMTP_PORT" not in found_keys:
            updated_lines.append(f"SMTP_PORT={smtp_port}")
        
        # Write back
        with open(env_path, "w") as f:
            f.write("\n".join(updated_lines))
        
        return {"status": "success", "message": "SMTP config updated. Restart the app for changes to take effect."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update SMTP config: {str(e)}")


@router.post("/test-smtp")
def test_smtp_connection(user_id: int = Depends(get_current_user_id)):
    """Attempt to login to the configured SMTP server (no mail sent).

    Useful to verify credentials (e.g. Gmail App Password) and server/port.
    """
    SMTP_USER = os.getenv("SMTP_USER", "your_email@gmail.com")
    SMTP_PASS = os.getenv("SMTP_PASS", "your_app_password")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

    if SMTP_USER == "your_email@gmail.com":
        raise HTTPException(status_code=400, detail=(
            "SMTP not configured. Set SMTP_USER and SMTP_PASS in backend/.env. "
            "For Gmail, generate a 16-character App Password (Account -> Security -> App passwords)."
        ))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.login(SMTP_USER, SMTP_PASS)
        return {"status": "success", "message": "SMTP login successful"}
    except smtplib.SMTPAuthenticationError as e:
        raise HTTPException(status_code=401, detail=(
            "SMTP authentication failed. Check SMTP_USER and SMTP_PASS (App Password for Gmail). "
            f"Provider message: {str(e)}"
        ))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SMTP connection failed: {str(e)}")


@router.get("/debug-token")
def debug_token(authorization: str = Header(None)):
    """Development helper: return the raw Authorization header and decoded JWT payload.

    Useful to debug why `/auth/profile` returns 401: missing header, malformed token,
    expired token, or secret mismatch.
    """
    result = {"authorization": authorization}
    if not authorization:
        result["error"] = "Missing Authorization header"
        return result

    parts = authorization.split()
    if len(parts) != 2:
        result["error"] = "Invalid Authorization header format"
        return result

    token = parts[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        result["payload"] = payload
        return result
    except ExpiredSignatureError:
        result["error"] = "Token expired"
        return result
    except JWTError as e:
        result["error"] = f"Invalid token: {str(e)}"
        return result


@router.get("/debug-secrets")
def debug_secrets():
    """Development helper: return hashes of the SECRET_KEY values seen by auth module and this module.

    This helps detect whether modules read different SECRET_KEY values at import time.
    """
    a = auth_module.SECRET_KEY if hasattr(auth_module, 'SECRET_KEY') else None
    b = SECRET_KEY
    def h(v):
        if v is None:
            return None
        return hashlib.sha256(v.encode('utf-8')).hexdigest()
    return {"auth_secret_sha256": h(a), "user_routes_secret_sha256": h(b)}
