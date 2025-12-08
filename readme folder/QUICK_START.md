# Quick Start Guide - Subscription Reminder System

## ⚡ 5-Minute Setup

### 1. Install Dependencies (one-time)
```powershell
cd o:\subscription_reminder
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Email (`.env` file)
Create or update `backend/.env`:
```
SECRET_KEY=change_me_to_a_random_secret_key_123456789
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password_16_chars
ALERT_OFFSETS=30,25,20,10
```

**For Gmail:**
- Use [App Password](https://myaccount.google.com/apppasswords), not your regular password
- [Enable 2-Factor Authentication](https://myaccount.google.com/security) first

### 3. Start Backend (Terminal 1)
```powershell
cd o:\subscription_reminder
.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 4. Start Frontend (Terminal 2)
```powershell
cd o:\subscription_reminder
python -m http.server 5173 --directory .
```

Expected output:
```
Serving HTTP on 0.0.0.0 port 5173
```

### 5. Open in Browser
- **Home**: http://localhost:5173/frontend/register.html
- **Dashboard** (after login): http://localhost:5173/frontend/home.html
- **Email Settings**: http://localhost:5173/frontend/email_settings.html
- **Database Viewer**: http://localhost:5173/frontend/database_viewer.html

---

## 🎯 Usage Flow

### First Time
1. Open `register.html` → Create account
2. Login with credentials
3. Go to **Email Settings** → Configure SMTP and send test email
4. Go to **Dashboard** → Add first subscription
5. Set renewal date 30+ days in future
6. Wait for scheduler to send alert (runs daily)
7. Check **Database Viewer** to see AlertLog entries

### Regular Use
1. Login on `login.html`
2. **Dashboard**: Add subscriptions, view upcoming renewals
3. **Email Settings**: Send test alerts, configure SMTP
4. **Database Viewer**: Monitor alert history

### API Testing
```powershell
# Get API info
curl http://127.0.0.1:8000

# Register
curl -X POST http://127.0.0.1:8000/auth/register `
  -H "Content-Type: application/json" `
  -d '{"email":"test@example.com","password":"Pass123!"}'

# Login (returns token)
curl -X POST http://127.0.0.1:8000/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"test@example.com","password":"Pass123!"}'

# Use token for protected endpoints
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  http://127.0.0.1:8000/auth/profile
```

---

## 📋 Environment Variables

| Variable | Required | Default | Example |
|----------|----------|---------|---------|
| `SECRET_KEY` | Yes | - | `my_secret_key_12345` |
| `SMTP_SERVER` | Yes | smtp.gmail.com | `smtp.gmail.com` |
| `SMTP_PORT` | Yes | 465 | `465` |
| `SMTP_USER` | Yes | - | `myemail@gmail.com` |
| `SMTP_PASS` | Yes | - | `xyza bcde fghi jklm` (16 chars) |
| `ALERT_OFFSETS` | No | 30,25,20,10 | `30,25,20,10` |

---

## ✅ Verification Checklist

- [ ] Backend running (http://127.0.0.1:8000 responds)
- [ ] Frontend running (http://localhost:5173 loads)
- [ ] Can register new account
- [ ] Can login and get JWT token
- [ ] Can add subscription
- [ ] Can send test email
- [ ] Can view database entries
- [ ] Logout button works

---

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Activate virtual environment first
.venv\Scripts\Activate.ps1

# Then run uvicorn
python -m uvicorn backend.main:app --reload --port 8000
```

### "Address already in use" error
```powershell
# Port 8000 already in use. Find and kill process:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Or use different port:
python -m uvicorn backend.main:app --port 8001
```

### Frontend won't load
```powershell
# Port 5173 already in use:
python -m http.server 5174 --directory .
# Then open http://localhost:5174/frontend/home.html
```

### Email not sending
1. Check `.env` file exists with SMTP credentials
2. Test with `POST /auth/send-test-email` endpoint
3. Verify SMTP credentials are correct
4. Check if Gmail requires App Password (not regular password)
5. Restart backend after updating `.env`

### Database error
```powershell
# Remove old database and start fresh:
cd backend
rm subscriptions.db
cd ..
# Restart backend - database will be recreated
```

---

## 🔑 API Endpoints Summary

### Authentication
- `POST /auth/register` - Create account
- `POST /auth/login` - Get JWT token
- `GET /auth/profile` - Get user info
- `PUT /auth/profile` - Update preferences
- `POST /auth/send-test-email` - Send test alert
- `POST /auth/smtp-config` - Update SMTP settings

### Subscriptions
- `POST /subscription/add` - Create subscription
- `GET /subscription/list` - List all subscriptions
- `PUT /subscription/update/{id}` - Update subscription
- `DELETE /subscription/delete/{id}` - Delete subscription
- `POST /subscription/send-alert/{id}` - Send alert now

---

## 📚 Documentation Files

- **README.md** - Full documentation (7000+ words)
- **COMPLETION_SUMMARY.md** - This session's achievements
- **QUICK_START.md** - This file (quick setup)

---

## ⏱️ Scheduler Details

The system sends email alerts on this schedule (default):
- **30 days** before renewal
- **25 days** before renewal
- **20 days** before renewal
- **10 days** before renewal

**Example**: Subscription renews on Feb 1, 2024:
- Jan 2: Alert #1 (30 days before)
- Jan 7: Alert #2 (25 days before)
- Jan 12: Alert #3 (20 days before)
- Jan 22: Alert #4 (10 days before)

No duplicate emails are sent (tracked by AlertLog table).

---

## 💾 Database Location

- **File**: `backend/subscriptions.db`
- **Format**: SQLite
- **Auto-created**: Yes (on first startup)
- **Size**: Small (~100KB for 1000 subscriptions)

---

## 🔒 Security Notes

- All passwords hashed with Argon2 (no 72-byte limit)
- JWT tokens expire after 24 hours
- SMTP credentials stored in `.env` (not in code)
- JWT secret stored in `.env` (not hardcoded)
- No sensitive data in database (passwords hashed)

---

## 🚀 Next Steps After Setup

1. **Add sample subscription** via dashboard
2. **Send test email** via email_settings.html
3. **Monitor database** via database_viewer.html
4. **Configure SMTP** via `/auth/smtp-config` API
5. **Wait for scheduler** to run (or restart backend to trigger immediately)

---

**Need help?** Check:
- Browser console (Ctrl+Shift+I) for frontend errors
- Terminal output for backend errors
- `subscriptions.db` file exists
- `.env` file has correct SMTP credentials

**Ready to deploy?** See README.md → Production Deployment section

---

*Built with ❤️ using FastAPI + SQLAlchemy + Bootstrap 5*
