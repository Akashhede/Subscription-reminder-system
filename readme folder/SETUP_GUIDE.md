# 🔔 Subscription Reminder System - Complete Setup & Usage Guide

## ✅ What's Been Implemented

### Backend Features
- ✅ User authentication with JWT tokens
- ✅ Password hashing with Argon2
- ✅ Email alerts system
- ✅ Database persistence with SQLite
- ✅ Subscription management (CRUD operations)
- ✅ Test email functionality
- ✅ Email preferences management
- ✅ Background scheduler for automatic reminders

### Frontend Features
- ✅ User registration page
- ✅ User login page
- ✅ Dashboard with subscription management
- ✅ Email settings page
- ✅ Database viewer page
- ✅ Responsive design with Bootstrap

### API Endpoints (18 total)
- Authentication: `/auth/register`, `/auth/login`, `/auth/profile`, `/auth/send-test-email`
- Subscriptions: `/subscription/add`, `/subscription/list`, `/subscription/send-alert/{id}`, `/subscription/update/{id}`, `/subscription/delete/{id}`

## 🚀 Quick Start

### 1. Start the Backend Server

```bash
cd o:\subscription_reminder
python -c "from backend.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000)"
```

**OR** use the simple command:
```bash
cd backend
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 2. Access the Frontend

Open in your browser:
- **Dashboard**: `file:///o:/subscription_reminder/frontend/home.html`
- **Register**: `file:///o:/subscription_reminder/frontend/register.html`
- **Login**: `file:///o:/subscription_reminder/frontend/login.html`
- **Email Settings**: `file:///o:/subscription_reminder/frontend/email_settings.html`
- **Database Viewer**: `file:///o:/subscription_reminder/frontend/database_viewer.html`

**OR** use a local server:
```bash
cd frontend
python -m http.server 8080
```
Then open: `http://localhost:8080/home.html`

### 3. Configure Email (Optional)

Create or edit `backend/.env`:
```ini
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```

**For Gmail:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to https://myaccount.google.com/apppasswords
4. Generate and copy the app password
5. Paste in `.env` file

## 📋 User Workflow

### Step 1: Register
1. Open `register.html`
2. Enter email and password
3. Click "Register"

### Step 2: Login
1. Open `login.html`
2. Enter credentials
3. Token is saved to browser localStorage

### Step 3: Add Subscriptions
1. Go to dashboard (`home.html`)
2. Fill subscription details:
   - Name (e.g., Netflix, Spotify)
   - Renewal Date
   - Note (optional)
3. Click "Add Subscription"

### Step 4: Manage Email Settings (Optional)
1. Go to `email_settings.html`
2. View current email
3. Send test email to verify configuration
4. Enable/disable email alerts

### Step 5: View Database (Optional)
1. Go to `database_viewer.html`
2. View all subscriptions
3. Export as JSON
4. Send alerts
5. Delete subscriptions

## 🔌 API Testing

### Using cURL

**Register:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "phone": "1234567890"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Add Subscription:**
```bash
curl -X POST http://localhost:8000/subscription/add \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Netflix",
    "renewal_date": "2025-12-25",
    "note": "Monthly subscription"
  }'
```

**Send Test Email:**
```bash
curl -X POST http://localhost:8000/auth/send-test-email \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test Email",
    "message": "This is a test"
  }'
```

## 📁 Project Structure

```
o:\subscription_reminder\
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── database.py                # SQLite configuration
│   ├── models.py                  # Database models (User, Subscription)
│   ├── schemas.py                 # Pydantic request/response models
│   ├── auth.py                    # Password hashing & JWT
│   ├── crud.py                    # Database operations
│   ├── send_email.py              # Email sending logic
│   ├── send_whatsapp.py           # WhatsApp integration (stub)
│   ├── reminder_job.py            # Background scheduler
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables (create this)
│   ├── subscriptions.db           # SQLite database (auto-created)
│   └── routes/
│       ├── __init__.py
│       ├── user_routes.py         # Auth & user endpoints
│       └── subscription_routes.py # Subscription endpoints
├── frontend/
│   ├── home.html                  # Dashboard
│   ├── register.html              # Registration
│   ├── login.html                 # Login
│   ├── email_settings.html        # Email config
│   └── database_viewer.html       # Database browser
├── EMAIL_SETUP.md                 # Email configuration guide
└── README.md
```

## 🛠️ Troubleshooting

### Server Won't Start
- Check port 8000 is not in use: `netstat -ano | findstr :8000`
- Kill process: `taskkill /PID <pid> /F`

### "Failed to fetch" Error in Frontend
- Make sure server is running on port 8000
- Check browser console for CORS errors
- Verify token is saved in localStorage

### Email Not Sending
- Check `.env` file exists and is configured
- Verify Gmail app password (not regular password)
- Check 2-Step Verification is enabled on Gmail account
- Look at uvicorn server logs for error messages

### Database Issues
- Delete `backend/subscriptions.db` to reset
- App will auto-create new database on startup

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  phone TEXT,
  email_alerts_enabled BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP
);
```

### Subscriptions Table
```sql
CREATE TABLE subscriptions (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  renewal_date DATE NOT NULL,
  note TEXT,
  user_id INTEGER FOREIGN KEY REFERENCES users(id)
);
```

## 🔐 Security Features

- ✅ Password hashing with Argon2
- ✅ JWT token-based authentication
- ✅ CORS middleware enabled
- ✅ Unique email constraint
- ✅ User isolation (subscriptions visible only to owner)
- ✅ Authorization checks on all endpoints

## 📦 Dependencies

```
fastapi==0.122.0
uvicorn[standard]==0.38.0
sqlalchemy==2.0.44
pydantic==2.12.4
python-jose==3.5.0
passlib==1.8.0
argon2-cffi==23.1.0
python-multipart==0.0.20
python-dotenv
email-validator
apscheduler==3.11.1
requests
Jinja2
```

## 🎯 Next Steps

1. **Production Deployment:**
   - Use environment variables for secrets
   - Deploy to cloud (Heroku, AWS, Azure, etc.)
   - Use PostgreSQL instead of SQLite
   - Add HTTPS/SSL

2. **Features to Add:**
   - WhatsApp integration
   - SMS alerts
   - Multiple notification methods
   - Email templates
   - Recurring subscriptions
   - Subscription categories
   - Export/Import functionality

3. **Improvements:**
   - Add unit tests
   - Add API documentation
   - Improve UI/UX
   - Add dark mode
   - Mobile app (React Native)

## 📞 Support

For issues or questions, check:
1. Browser console (F12) for frontend errors
2. Uvicorn server output for backend errors
3. `.env` file for configuration issues
4. `EMAIL_SETUP.md` for email configuration help

---

**Version**: 1.0.0  
**Created**: December 2, 2025  
**Status**: ✅ Ready for Testing
