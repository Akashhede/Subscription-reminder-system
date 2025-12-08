# Email Configuration Guide

You have two options for sending emails: **Gmail SMTP** or **SendGrid API**

## Option 1: Gmail SMTP (Recommended if you have Gmail)

### Prerequisites
- Gmail account with 2-Step Verification enabled

### Setup Steps

1. **Enable 2-Step Verification**
   - Go to https://myaccount.google.com/security
   - Click "2-Step Verification" and follow the setup

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select **Mail** and **Windows Computer**
   - Click **Generate**
   - Google shows a 16-character password like: `xhyw yenx ykyp ievw`
   - Copy this password

3. **Update `.env` file**
   ```env
   SMTP_USER=your-gmail@gmail.com
   SMTP_PASS=xhyw yenx ykyp ievw
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=465
   ```

4. **Restart backend**
   ```powershell
   taskkill /F /IM python.exe
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```

5. **Test SMTP**
   ```powershell
   $login = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/auth/login' `
     -ContentType 'application/json' `
     -Body (@{email='your-email@example.com';password='your-password'} | ConvertTo-Json)
   $token = $login.access_token
   
   Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/auth/test-smtp' `
     -Headers @{Authorization="Bearer $token"}
   ```

---

## Option 2: SendGrid API

### Prerequisites
- SendGrid account (free tier available)

### Setup Steps

1. **Install SendGrid SDK**
   ```powershell
   pip install sendgrid
   ```

2. **Create SendGrid Account**
   - Go to https://sendgrid.com
   - Sign up for free account
   - Verify you can receive emails (usually auto-verified)

3. **Generate API Key**
   - Go to https://app.sendgrid.com/settings/api_keys
   - Click "Create API Key"
   - Give it a name like "Subscription Reminder"
   - Copy the API key (only shown once)

4. **Verify Sender Email**
   - Go to https://app.sendgrid.com/settings/sender_auth
   - Click "Verify a Single Sender"
   - Add your email address and verify it

5. **Update `.env` file**
   ```env
   SENDGRID_API_KEY=SG.xxxxx...xxxxx
   SENDGRID_FROM_EMAIL=your-verified@example.com
   ```

6. **Restart backend**
   ```powershell
   taskkill /F /IM python.exe
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```

7. **Test SendGrid**
   ```powershell
   $login = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/auth/login' `
     -ContentType 'application/json' `
     -Body (@{email='your-email@example.com';password='your-password'} | ConvertTo-Json)
   $token = $login.access_token
   
   Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/auth/send-test-email' `
     -Headers @{Authorization="Bearer $token";"Content-Type"="application/json"} `
     -Body (@{subject='Test';message='SendGrid test email'} | ConvertTo-Json)
   ```

---

## Switching Between Gmail and SendGrid

The application automatically uses the first available method:

1. **Gmail SMTP** (if `SMTP_USER` is configured)
2. **SendGrid** (if `SENDGRID_API_KEY` is configured)
3. **Fallback**: If SMTP fails, automatically tries SendGrid

To use **only Gmail**:
- Configure `SMTP_USER`, `SMTP_PASS`, `SMTP_SERVER`, `SMTP_PORT`
- Leave `SENDGRID_API_KEY` blank

To use **only SendGrid**:
- Leave `SMTP_USER` as default or empty
- Configure `SENDGRID_API_KEY` and `SENDGRID_FROM_EMAIL`

---

## Troubleshooting

### Gmail SMTP: 535 BadCredentials
- Confirm 2-Step Verification is enabled
- Generate a **new** App Password (old ones may expire)
- Paste the exact 16-character password into `SMTP_PASS`
- Some Gmail accounts block "Less secure apps" - use App Password instead

### SendGrid: API Key Invalid
- Verify the API key starts with `SG.`
- Copy the full key without spaces
- Confirm the sender email is verified in SendGrid

### Email not received
- Check spam/junk folder
- Verify sender email is correct
- Check SendGrid dashboard → Email Activity for delivery status
- Verify recipient email is correct

---

## Best Practices

- **Gmail**: Good for personal use, limited to ~100 emails/day
- **SendGrid**: Better for production, up to 40,000 emails/month free
- **Both configured**: Falls back automatically if one fails
- **Security**: Never commit `.env` with real credentials to git

---

## Environment Variables Summary

| Variable | Example | Required | Notes |
|----------|---------|----------|-------|
| `SMTP_USER` | `user@gmail.com` | No (use either SMTP or SendGrid) | Gmail address |
| `SMTP_PASS` | `xhyw yenx ykyp ievw` | No (if SMTP_USER set) | 16-char Gmail App Password |
| `SMTP_SERVER` | `smtp.gmail.com` | No (default: `smtp.gmail.com`) | SMTP server address |
| `SMTP_PORT` | `465` | No (default: `465`) | SMTP port (usually 465 for SSL) |
| `SENDGRID_API_KEY` | `SG.xxxxxxxxx...` | No (use either SMTP or SendGrid) | SendGrid API key |
| `SENDGRID_FROM_EMAIL` | `noreply@example.com` | No (if SENDGRID_API_KEY set) | Verified sender email |

---

## Example `.env` Files

### Gmail SMTP Only
```env
SMTP_USER=myemail@gmail.com
SMTP_PASS=xhyw yenx ykyp ievw
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SECRET_KEY=your-secret-key
```

### SendGrid Only
```env
SENDGRID_API_KEY=SG.xxx...xxx
SENDGRID_FROM_EMAIL=noreply@example.com
SECRET_KEY=your-secret-key
```

### Both (Fallback)
```env
SMTP_USER=myemail@gmail.com
SMTP_PASS=xhyw yenx ykyp ievw
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDGRID_API_KEY=SG.xxx...xxx
SENDGRID_FROM_EMAIL=noreply@example.com
SECRET_KEY=your-secret-key
```
