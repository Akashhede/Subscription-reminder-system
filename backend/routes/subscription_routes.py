from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.schemas import SubscriptionCreate, SubscriptionOut, AlertResponse
from backend import crud
from backend.send_email import send_email_alert
from backend.models import User, Subscription
from typing import List
from jose import jwt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(authorization: str = Header(None)):
    # Very simple token decode: expects "Bearer <token>"
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")
    parts = authorization.split()
    if len(parts) != 2: raise HTTPException(status_code=401, detail="Invalid auth header")
    token = parts[1]
    try:
        payload = jwt.decode(token, "change_me_to_a_random_secret", algorithms=["HS256"])
        return int(payload.get("user_id"))
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/add", response_model=SubscriptionOut)
def add_subscription(sub: SubscriptionCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    created = crud.create_subscription(db, user_id, sub.name, sub.renewal_date, sub.note)
    return created

@router.get("/list", response_model=List[SubscriptionOut])
def list_subscriptions(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return crud.get_subscriptions_for_user(db, user_id)

@router.post("/send-alert/{subscription_id}", response_model=AlertResponse)
def send_subscription_alert(subscription_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """Send an email alert for a specific subscription"""
    subscription = crud.get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if subscription.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        subject = f"Subscription Renewal Alert: {subscription.name}"
        message = f"""
Hello {user.email},

This is a reminder that your subscription '{subscription.name}' needs to be renewed.

Renewal Date: {subscription.renewal_date}
Notes: {subscription.note or 'No additional notes'}

Please take action to renew your subscription before the renewal date.

Best regards,
Subscription Reminder Service
"""
        send_email_alert(user.email, subject, message)
        return {"status": "success", "message": f"Alert email sent to {user.email}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@router.put("/update/{subscription_id}", response_model=SubscriptionOut)
def update_subscription(subscription_id: int, sub: SubscriptionCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    existing_sub = crud.get_subscription(db, subscription_id)
    if not existing_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if existing_sub.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this subscription")
    
    updated = crud.update_subscription(db, subscription_id, sub.name, sub.renewal_date, sub.note)
    return updated

@router.delete("/delete/{subscription_id}", response_model=SubscriptionOut)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    existing_sub = crud.get_subscription(db, subscription_id)
    if not existing_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if existing_sub.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this subscription")

    crud.delete_subscription(db, subscription_id)
    return existing_sub
