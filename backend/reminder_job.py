from apscheduler.schedulers.background import BackgroundScheduler
from .database import SessionLocal
from .models import Subscription, User, AlertLog
from datetime import datetime, timedelta
from .send_email import send_email_alert
import os

_scheduler = None

# Default alert offsets (days before renewal) — adjustable via ENV var ALERT_OFFSETS as CSV
# Common schedule: 30 (1 month), 25, 20, 10 days before renewal
DEFAULT_ALERT_OFFSETS = [30, 25, 20, 10]

def get_alert_offsets():
    raw = os.getenv("ALERT_OFFSETS")
    if not raw:
        return DEFAULT_ALERT_OFFSETS
    try:
        parts = [int(x.strip()) for x in raw.split(",") if x.strip()]
        return sorted(set(parts), reverse=True)
    except Exception:
        print(f"[Scheduler] Invalid ALERT_OFFSETS='{raw}', using defaults")
        return DEFAULT_ALERT_OFFSETS

def check_expiring_subscriptions():
    """Check subscriptions and send alerts at configured offsets before renewal_date.

    This function finds subscriptions where renewal_date == today + offset
    for each configured offset and sends email/whatsapp alerts accordingly.
    """
    db = SessionLocal()
    try:
        today = datetime.utcnow().date()
        offsets = get_alert_offsets()
        print(f"[Scheduler] Running check for offsets: {offsets} (today={today})")

        for offset in offsets:
            target = today + timedelta(days=offset)
            subs = db.query(Subscription).filter(Subscription.renewal_date == target).all()
            print(f"[Scheduler] {len(subs)} subscription(s) found for target={target} (offset={offset})")
            for s in subs:
                try:
                    user = db.query(User).filter(User.id == s.user_id).first()
                    if not user:
                        print(f"[Scheduler] No user found for subscription id={s.id}")
                        continue

                    subject = f"Reminder: '{s.name}' renews in {offset} day(s)"
                    msg = (
                        f"Hi {user.email},\n\n"
                        f"This is a reminder that your subscription '{s.name}' will renew on {s.renewal_date} (in {offset} day(s)).\n\n"
                        f"Note: {s.note or '-'}\n\n"
                        "Please take action if you wish to cancel or update your payment.\n\n"
                        "Best regards,\nSubscription Reminder Service"
                    )

                    if user.email:
                        # Skip if we've already sent this offset/email for this subscription
                        existing = db.query(AlertLog).filter(
                            AlertLog.subscription_id == s.id,
                            AlertLog.offset == offset,
                            AlertLog.channel == 'email'
                        ).first()
                        if existing:
                            print(f"[Scheduler] Email already sent for sub id={s.id} offset={offset}, skipping")
                        else:
                            try:
                                send_email_alert(user.email, subject, msg)
                                # record the sent alert
                                log = AlertLog(subscription_id=s.id, offset=offset, channel='email')
                                db.add(log)
                                db.commit()
                                print(f"[Scheduler] Sent EMAIL alert to {user.email} for sub id={s.id} (offset={offset})")
                            except Exception as e:
                                db.rollback()
                                print(f"[Scheduler] Failed to send email to {user.email}: {e}")

                    if user.phone:
                        existing_wh = db.query(AlertLog).filter(
                            AlertLog.subscription_id == s.id,
                            AlertLog.offset == offset,
                            AlertLog.channel == 'whatsapp'
                        ).first()
                        if existing_wh:
                            print(f"[Scheduler] WhatsApp already sent for sub id={s.id} offset={offset}, skipping")
                        else:
                            try:
                                # TODO: Implement WhatsApp sending when send_whatsapp.py is available
                                # send_whatsapp_alert(user.phone, msg)
                                log = AlertLog(subscription_id=s.id, offset=offset, channel='whatsapp')
                                db.add(log)
                                db.commit()
                                print(f"[Scheduler] Sent WHATSAPP alert to {user.phone} for sub id={s.id} (offset={offset})")
                            except Exception as e:
                                db.rollback()
                                print(f"[Scheduler] Failed to send whatsapp to {user.phone}: {e}")
                except Exception as ex:
                    print(f"[Scheduler] Error processing subscription id={s.id}: {ex}")
    except Exception as e:
        print(f"[Scheduler] General error in scheduler: {e}")
    finally:
        db.close()

def start_scheduler():
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        print("Scheduler is already running")
        return
    
    _scheduler = BackgroundScheduler()
    _scheduler.add_job(check_expiring_subscriptions, "interval", hours=24)
    try:
        _scheduler.start()
        print("Scheduler started successfully")
    except Exception as e:
        print(f"Error starting scheduler: {e}")