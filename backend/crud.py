
from sqlalchemy.orm import Session
from . import models, auth
from datetime import date

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email==email).first()

def create_user(db: Session, email: str, password: str, phone: str = None):
    hashed = auth.hash_password(password)
    user = models.User(email=email, hashed_password=hashed, phone=phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user: return None
    if not auth.verify_password(password, user.hashed_password): return None
    return user

def create_subscription(db: Session, user_id: int, name: str, renewal_date: date, note: str = None, start_date: date = None):
    sub = models.Subscription(name=name, renewal_date=renewal_date, note=note, start_date=start_date, user_id=user_id)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

def get_subscriptions_for_user(db: Session, user_id: int):
    return db.query(models.Subscription).filter(models.Subscription.user_id==user_id).all()

def get_subscription(db: Session, subscription_id: int):
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()

def update_subscription(db: Session, subscription_id: int, name: str, renewal_date: date, note: str = None, start_date: date = None):
    sub = get_subscription(db, subscription_id)
    if sub:
        sub.name = name
        sub.renewal_date = renewal_date
        sub.note = note
        sub.start_date = start_date
        db.commit()
        db.refresh(sub)
    return sub

def delete_all_subscriptions_for_user(db: Session, user_id: int):
    """Delete all subscriptions for a user"""
    db.query(models.Subscription).filter(models.Subscription.user_id == user_id).delete()
    db.commit()
    return True

def delete_subscription(db: Session, subscription_id: int):
    sub = get_subscription(db, subscription_id)
    if sub:
        db.delete(sub)
        db.commit()
    return sub
