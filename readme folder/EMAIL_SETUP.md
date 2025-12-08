# Subscription Reminder System - Email Configuration Guide

## Features

- 📧 **Email Alerts**: Receive email notifications for subscription renewals
- 💬 **WhatsApp Alerts**: Get WhatsApp messages (optional)
- 🔔 **Smart Reminders**: Automatic notifications 10 days before expiry
- 🔐 **Secure**: Password-protected accounts with JWT authentication

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Email (Gmail Example)

#### Step 1: Enable 2-Step Verification
1. Go to https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow the setup process

#### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer" (or your device)
3. Click "Generate"
4. Copy the 16-character password

#### Step 3: Create `.env` file in backend folder

```bash
# backend/.env
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```

**Replace:**
- `your_email@gmail.com` with your Gmail address
- `your_app_password` with the 16-character password from step 2

### 3. Start the Application

```bash
# Terminal 1: Start Backend API
cd backend
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Open Frontend
# Simply open the HTML files in your browser
# Or use a local server:
python -m http.server 8080 --directory frontend
```

### 4. Access the Application

- **Frontend**: http://localhost:8080 (if using http.server)
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Using Email Features

### Register & Login
1. Open `register.html` or `login.html`
2. Create an account or login with your email

### Configure Email Settings
1. After logging in, click the "📧 Email Settings" button
2. View your current email address
3. Send a test email to verify configuration
4. Enable/disable email alerts as needed

### Send Test Email
1. Go to Email Settings page
2. Fill in the subject and message
3. Click "Send Test Email ✉️"
4. Check your inbox to verify email configuration works

### Add Subscriptions
1. On the Dashboard, fill in subscription details:
   - **Name**: Subscription name (e.g., Netflix)
   - **Renewal Date**: When the subscription renews
   - **Note**: Optional notes
2. Click "Add Subscription"

### Manual Email Alert
1. View your subscriptions on the dashboard
2. Click "📧 Send Alert" button for any subscription
3. An email will be sent immediately to your registered email

### Automatic Alerts
- The system automatically checks subscriptions daily
- 10 days before renewal date, an email alert is sent
- Notifications are sent based on your email preferences

## API Endpoints

### Authentication
- `POST /auth/register` - Create new account
- `POST /auth/login` - Login to account
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user preferences
- `POST /auth/send-test-email` - Send test email

### Subscriptions
- `POST /subscription/add` - Add new subscription
- `GET /subscription/list` - List all subscriptions
- `PUT /subscription/update/{id}` - Update subscription
- `DELETE /subscription/delete/{id}` - Delete subscription
- `POST /subscription/send-alert/{id}` - Send alert for subscription

## Testing with cURL

### Send Test Email
```bash
curl -X POST http://localhost:8000/auth/send-test-email \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test Email",
    "message": "This is a test email"
  }'
```

### Send Alert for Subscription
```bash
curl -X POST http://localhost:8000/subscription/send-alert/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Troubleshooting

### Email Not Sending
1. **Check Gmail security**: https://myaccount.google.com/security/checkup
2. **Verify app password**: Make sure you're using the 16-character password, not your Gmail password
3. **Check SMTP settings**: Open backend/send_email.py and verify settings
4. **Check logs**: Look at the uvicorn server output for error messages

### Test Email Endpoint Not Working
1. Make sure you're authenticated (logged in)
2. Check that email alerts are enabled in settings
3. Verify your email address is correct in the profile

### Port Already in Use
- Change the port: `python -m uvicorn backend.main:app --port 9000`
- Or find and stop the process using port 8000

## Using Different Email Providers

### Outlook/Hotmail
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your_email@outlook.com
SMTP_PASS=your_password
```

### SendGrid (Recommended for Production)
```
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=SG.your_sendgrid_api_key
```

## Environment Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `SMTP_USER` | user@gmail.com | Email address to send from |
| `SMTP_PASS` | xxxx xxxx xxxx xxxx | App password (16 chars for Gmail) |
| `SMTP_SERVER` | smtp.gmail.com | SMTP server address |
| `SMTP_PORT` | 465 | SMTP port (465 for SSL, 587 for TLS) |

## Project Structure

```
subscription_reminder/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── auth.py                 # Password hashing & JWT
│   ├── crud.py                 # Database operations
│   ├── send_email.py           # Email sending logic
│   ├── send_whatsapp.py        # WhatsApp logic (optional)
│   ├── reminder_job.py         # Background scheduler
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (create this)
│   └── routes/
│       ├── user_routes.py      # User authentication endpoints
│       └── subscription_routes.py # Subscription endpoints
├── frontend/
│   ├── home.html               # Dashboard
│   ├── register.html           # Registration page
│   ├── login.html              # Login page
│   └── email_settings.html     # Email configuration page
└── README.md
```

## Features Coming Soon

- [ ] WhatsApp integration
- [ ] SMS alerts
- [ ] Push notifications
- [ ] Custom alert times
- [ ] Multiple notification methods
- [ ] Email templates

## Support

For issues or questions, check the logs in the uvicorn terminal or open an issue in the repository.

---

**Version**: 1.0.0  
**Last Updated**: December 2, 2025
