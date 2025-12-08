
# Subscription Reminder System
**FastAPI + SQLite + Bootstrap 5 Frontend with Multi-Offset Email Scheduler**

## 📋 Overview

A complete subscription management and automated reminder system:
- **Backend**: FastAPI + Uvicorn + SQLAlchemy ORM + APScheduler
- **Database**: SQLite with User, Subscription, and AlertLog models
- **Frontend**: Bootstrap 5.3 + Vanilla JavaScript (Register, Login, Dashboard)
- **Authentication**: JWT tokens with Argon2 password hashing (no 72-byte limit)
- **Email Alerts**: SMTP integration with configurable multi-offset scheduling (30, 25, 20, 10 days before renewal)
- **Deduplication**: AlertLog prevents duplicate email sends

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- SMTP server credentials (Gmail, Office365, etc.)

### Setup

1. **Create virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment (`.env` file):**
   ```
   SECRET_KEY=your_super_secret_jwt_key_change_me_in_production
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=465
   SMTP_USER=your_email@gmail.com
   SMTP_PASS=your_app_password
   ALERT_OFFSETS=30,25,20,10
   ```
   
   **Note**: For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.

4. **Start backend server:**
   ```powershell
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   Server runs at `http://127.0.0.1:8000`

5. **Serve frontend (in another terminal):**
   ```powershell
   python -m http.server 5173 --directory .
   ```
   Open `http://localhost:5173/frontend/home.html`

## 📖 Features

### Authentication
- **Register**: Email + Password (stored with Argon2 hashing)
- **Login**: Returns JWT token (valid for 24 hours)
- **Profile**: View and update user preferences

### Subscription Management
- **Add Subscription**: Name, renewal date, notes
- **List**: View all user subscriptions
- **Update/Delete**: Modify or remove subscriptions
- **Send Alert**: Manually trigger email alert

### Email Alerts
- **Scheduler**: APScheduler runs daily, checks subscriptions at configured offsets
- **Multi-Offset**: Default 30, 25, 20, 10 days before renewal date
- **Deduplication**: AlertLog table tracks sent alerts (prevents duplicate emails)
- **Test Email**: Send test alert from UI or API

### Email Configuration (NEW)
- **UI**: Email Settings page (`frontend/email_settings.html`)
- **API**: `POST /auth/smtp-config` - Update SMTP credentials without restarting
- **Database Viewer**: View all users, subscriptions, and sent alerts

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (returns JWT)
- `GET /auth/profile` - Get current user info
- `PUT /auth/profile` - Update email preferences
- `POST /auth/send-test-email` - Send test alert
- `POST /auth/smtp-config` - Update SMTP settings (NEW)

### Subscriptions
- `POST /subscription/add` - Create subscription
- `GET /subscription/list` - List user subscriptions
- `PUT /subscription/update/{id}` - Update subscription
- `DELETE /subscription/delete/{id}` - Delete subscription
- `POST /subscription/send-alert/{id}` - Manually send alert

## 📁 Project Structure

```
subscription_reminder/
├── backend/
│   ├── main.py              # FastAPI app initialization
│   ├── models.py            # SQLAlchemy ORM (User, Subscription, AlertLog)
│   ├── schemas.py           # Pydantic request/response models
│   ├── auth.py              # JWT + Argon2 password hashing
│   ├── crud.py              # Database operations
│   ├── database.py          # SQLAlchemy session + table creation
│   ├── send_email.py        # SMTP email sending
│   ├── send_whatsapp.py     # WhatsApp placeholder (Twilio)
│   ├── reminder_job.py      # APScheduler multi-offset scheduler
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Configuration (SMTP, JWT, offsets)
│   └── routes/
│       ├── user_routes.py   # Auth endpoints
│       └── subscription_routes.py  # Subscription endpoints
├── frontend/
│   ├── home.html            # Dashboard (after login)
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── email_settings.html  # Email configuration (NEW)
│   └── database_viewer.html # View all database records (NEW)
└── README.md                # This file
```

## 🔐 Database Models

### User
```python
- id: Integer (Primary Key)
- email: String (Unique)
- hashed_password: String (Argon2)
- phone: String (optional)
- email_alerts_enabled: Boolean (default True)
- created_at: DateTime
```

### Subscription
```python
- id: Integer (Primary Key)
- name: String
- renewal_date: Date
- note: String (optional)
- user_id: Integer (Foreign Key → User)
- created_at: DateTime
```

### AlertLog
```python
- id: Integer (Primary Key)
- subscription_id: Integer (Foreign Key → Subscription)
- offset: Integer (days before renewal)
- channel: String (email/whatsapp)
- sent_at: DateTime
```

## ⏱️ Scheduler Details

The `reminder_job.py` scheduler:
1. Runs every 24 hours (daily at startup)
2. Checks all subscriptions for upcoming renewals
3. Uses `ALERT_OFFSETS` (default: 30,25,20,10 days)
4. Queries `AlertLog` to prevent duplicate sends
5. Sends SMTP email if configured and not previously sent

**Example**: For a subscription renewing on 2024-02-01:
- Day 2024-01-02: Email sent (30 days before)
- Day 2024-01-07: Email sent (25 days before)
- Day 2024-01-12: Email sent (20 days before)
- Day 2024-01-22: Email sent (10 days before)

## 🛠️ Configuration

### `.env` Variables
| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `SECRET_KEY` | Yes | `change_me_to_a_random_secret` | JWT signing key (change in production) |
| `SMTP_SERVER` | Yes | `smtp.gmail.com` | SMTP server hostname |
| `SMTP_PORT` | Yes | `465` | SMTP port (465=SSL, 587=TLS) |
| `SMTP_USER` | Yes | - | Email address to send from |
| `SMTP_PASS` | Yes | - | Email password or app password |
| `ALERT_OFFSETS` | No | `30,25,20,10` | Comma-separated days before renewal |

### Gmail Configuration (Recommended)
1. Enable 2-Factor Authentication on your Gmail account
2. Generate [App Password](https://myaccount.google.com/apppasswords)
3. Use the 16-character password in `.env` as `SMTP_PASS`

## 🧪 Testing

### Manual API Test (PowerShell)
```powershell
# Register
$body = @{
    email = "test@example.com"
    password = "SecurePass123!"
}
Invoke-WebRequest -Uri "http://127.0.0.1:8000/auth/register" `
    -Method POST -ContentType "application/json" `
    -Body (ConvertTo-Json $body)

# Login
$login = @{
    email = "test@example.com"
    password = "SecurePass123!"
}
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/auth/login" `
    -Method POST -ContentType "application/json" `
    -Body (ConvertTo-Json $login)
$token = ($response.Content | ConvertFrom-Json).access_token

# Add Subscription
$sub = @{
    name = "Netflix"
    renewal_date = "2024-02-15"
    note = "Monthly subscription"
}
Invoke-WebRequest -Uri "http://127.0.0.1:8000/subscription/add" `
    -Method POST -ContentType "application/json" `
    -Headers @{"Authorization" = "Bearer $token"} `
    -Body (ConvertTo-Json $sub)
```

### UI Testing
1. Open `http://localhost:5173/frontend/register.html`
2. Create account
3. Login on `http://localhost:5173/frontend/login.html`
4. Add subscription on dashboard
5. Go to Email Settings (`email_settings.html`) to configure SMTP and send test email
6. Check "Database Viewer" for alert logs

## 📦 Dependencies

**Core**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `python-dotenv` - Environment configuration

**Authentication**
- `python-jose` - JWT handling
- `argon2-cffi` - Password hashing

**Scheduling**
- `apscheduler` - Background job scheduler

**Email**
- Built-in `smtplib` (Python standard library)

## ⚠️ Production Deployment

1. **Security**
   - Set `SECRET_KEY` to a cryptographically secure random string
   - Use environment variables instead of `.env` file
   - Enable HTTPS/TLS for all communication
   - Use app passwords (not account passwords) for SMTP

2. **Scheduler**
   - Run scheduler in separate worker (e.g., Celery + Redis)
   - Consider using managed email service (SendGrid, AWS SES)
   - Implement retry logic and error logging

3. **Database**
   - Use PostgreSQL or MySQL for production (not SQLite)
   - Enable automated backups
   - Set up connection pooling

4. **Server**
   - Use `gunicorn` or similar WSGI server (not `uvicorn --reload`)
   - Run behind reverse proxy (Nginx)
   - Set resource limits and monitoring

## 🐛 Troubleshooting

### "SMTP not configured"
- Ensure `.env` file exists with `SMTP_USER`, `SMTP_PASS`, `SMTP_SERVER`, `SMTP_PORT`
- Restart the server after updating `.env`

### "Failed to fetch" in frontend
- Ensure backend is running (`http://127.0.0.1:8000` returns JSON)
- Check browser console for CORS errors
- Verify JWT token is valid (check localStorage in browser dev tools)

### Scheduler not running
- Check APScheduler logs in terminal
- Verify subscription renewal_dates are set correctly
- Monitor `subscriptions.db` AlertLog table for sent alerts

### Email not sending
- Verify SMTP credentials are correct
- Check if Gmail requires App Password (not regular password)
- Test with `POST /auth/send-test-email` endpoint
- Monitor `backend/send_email.py` for exceptions

## 📝 Version History

**Latest Session Updates:**
- ✅ Added multi-offset scheduler (30, 25, 20, 10 days configurable)
- ✅ Added AlertLog model for deduplication
- ✅ Added email settings UI page
- ✅ Added database viewer page
- ✅ Added logout buttons
- ✅ Switched to Argon2 password hashing (fixes 72-byte limit)
- ✅ Removed duplicate code (TestEmailRequest consolidated)
- ✅ Removed debug prints
- ✅ Added SMTP config API endpoint (`POST /auth/smtp-config`)
- ✅ Consolidated JWT SECRET_KEY to environment variable

## 📧 Support

For issues or questions, check:
1. Browser console (Ctrl+Shift+I) for frontend errors
2. Terminal output for backend exceptions
3. Database file (`subscriptions.db`) for data consistency
4. Email headers in test emails for SMTP debugging

---

**Built with ❤️ using FastAPI + SQLAlchemy + Bootstrap**

