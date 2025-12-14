# SMTP Configuration Instructions

## Supported Email Providers

This system supports multiple email providers:
- **Gmail** (with App Password)
- **Hostinger** (Business Email)
- **Other SMTP providers** (custom configuration)

---

## Option 1: Hostinger Email Configuration (Recommended for Testing)

### Step 1: Get Hostinger Email Credentials
1. Log in to your Hostinger account
2. Go to **Email** → **Email Accounts**
3. Note your email address (e.g., `xxx@companyname.com`)
4. Use your email account password

### Step 2: Update .env File for Hostinger
Create or update `backend/.env` file with:

```env
SMTP_USER=xxx@companyname.com
SMTP_PASS=your_email_password
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=465
SMTP_USE_TLS=false
SECRET_KEY=subscription_reminder_secret_key_2024_prod
```

**Hostinger SMTP Settings:**
- **SMTP Server**: `smtp.hostinger.com`
- **Port**: `465` (SSL) or `587` (TLS)
- **Username**: Your full email address (e.g., `xxx@companyname.com`)
- **Password**: Your email account password
- **Security**: SSL (port 465) or TLS (port 587)

### Alternative Hostinger Configuration (TLS):
If port 465 doesn't work, try TLS on port 587:

```env
SMTP_USER=xxx@companyname.com
SMTP_PASS=your_email_password
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=587
SMTP_USE_TLS=true
```

---

## Option 2: Gmail Configuration

### Step 1: Verify Gmail App Password
1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification** (must be enabled)
3. Scroll down to **App passwords**
4. Generate a new App Password for "Mail" and "Other (Custom name)" → "Subscription Reminder"
5. Copy the 16-character password (it will look like: `abcd efgh ijkl mnop`)

### Step 2: Update .env File for Gmail
Create or update `backend/.env` file with:

```env
SMTP_USER=akashhede360@gmail.com
SMTP_PASS=your_16_character_app_password_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USE_TLS=false
SECRET_KEY=subscription_reminder_secret_key_2024_prod
```

**Important Notes:**
- Use the **App Password**, NOT your regular Gmail password
- Remove spaces from the App Password (e.g., `abcdefghijklmnop`)
- Make sure 2-Step Verification is enabled on your Google account

### Step 3: Restart Backend Server
After updating the `.env` file, restart your backend server:

```bash
cd backend
uvicorn main:app --reload
```

### Step 4: Test Email
1. Go to the home page
2. Use the "Test Email" form
3. Click "Send Test Email"
4. Check your email inbox (the email will be sent to `akashhede360@gmail.com` as priority recipient)

---

## Testing with Different Email Accounts

You can test with different email accounts by updating the SMTP configuration:

### For Hostinger (xxx@companyname.com):
```env
SMTP_USER=xxx@companyname.com
SMTP_PASS=your_hostinger_email_password
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=465
SMTP_USE_TLS=false
```

### For Gmail:
```env
SMTP_USER=akashhede360@gmail.com
SMTP_PASS=your_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USE_TLS=false
```

**Note**: All emails will still be sent to `akashhede360@gmail.com` as the priority recipient, but they will be sent FROM the configured SMTP account.

## Email Priority Configuration

**All emails are now configured to send to `akashhede360@gmail.com` as the priority recipient.**

The system will:
- Send all reminder emails to `akashhede360@gmail.com`
- Include the original user's email in the message body
- This ensures you receive all subscription reminders regardless of which user account created them

## Troubleshooting

### Hostinger-Specific Issues:
1. **Authentication Failed**: 
   - Make sure you're using the full email address as SMTP_USER (e.g., `xxx@companyname.com`)
   - Verify the password is correct (not your Hostinger account password, but the email account password)
   - Check if the email account is active in Hostinger panel

2. **Connection Issues**:
   - Try port 587 with TLS: Set `SMTP_PORT=587` and `SMTP_USE_TLS=true`
   - Check if your hosting provider blocks SMTP ports
   - Verify `smtp.hostinger.com` is accessible

3. **Port 465 vs 587**:
   - Port 465: SSL encryption (set `SMTP_USE_TLS=false`)
   - Port 587: TLS encryption (set `SMTP_USE_TLS=true`)

### Gmail-Specific Issues:
1. **Double-check App Password**: Make sure you're using the App Password, not your regular password
2. **Check 2FA**: Ensure 2-Step Verification is enabled
3. **Remove spaces**: App passwords often have spaces - remove them in the .env file

### General Issues:
1. **Check .env location**: Make sure the .env file is in the `backend/` directory
2. **Restart server**: Always restart after changing .env
3. **Check credentials**: Verify SMTP_USER and SMTP_PASS are correct
4. **Test connection**: Use the test email feature on the home page

### Common Errors:
- `535 Authentication failed`: Wrong password or incorrect credentials
- `Connection refused`: Check SMTP_SERVER and SMTP_PORT
- `Timeout`: Check your internet connection or firewall settings
- `SSL/TLS error`: Try switching between port 465 (SSL) and 587 (TLS)

## Verification

After configuration, you should see in the terminal:
```
Email sent successfully via SMTP (smtp.hostinger.com) to akashhede360@gmail.com
```
or
```
Email sent successfully via SMTP (smtp.gmail.com) to akashhede360@gmail.com
```

And receive the test email in your inbox at `akashhede360@gmail.com`.

## Quick Reference

### Hostinger Configuration:
```env
SMTP_USER=xxx@companyname.com
SMTP_PASS=your_email_password
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=465
SMTP_USE_TLS=false
```

### Gmail Configuration:
```env
SMTP_USER=akashhede360@gmail.com
SMTP_PASS=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USE_TLS=false
```

**Remember**: All emails are sent TO `akashhede360@gmail.com`, but they are sent FROM the configured SMTP account.

