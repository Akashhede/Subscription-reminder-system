
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email_alerts_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="owner")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    renewal_date = Column(Date, nullable=False)
    note = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="subscriptions")


class AlertLog(Base):
    __tablename__ = "alert_logs"
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    offset = Column(Integer, nullable=False)  # days before renewal when alert was sent
    channel = Column(String, nullable=False)  # 'email' or 'whatsapp'
    sent_at = Column(DateTime, default=datetime.utcnow)
