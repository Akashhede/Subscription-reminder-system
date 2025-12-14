# Fix Gmail SMTP Authentication (535 BadCredentials)

## Problem
The current `SMTP_PASS` in `.env` is invalid. Gmail rejected the login with error `535 BadCredentials`.

## Solution: Generate a Valid Gmail App Password

### Step 1: Ensure 2-Step Verification is Enabled
1. Go to https://myaccount.google.com/security
2. Scroll down to "How you sign in to Google"
3. Click "2-Step Verification"
4. If not enabled, follow the prompts to enable it (you'll need your phone)

### Step 2: Generate an App Password
1. After 2FA is enabled, go to https://myaccount.google.com/apppasswords
2. You should see a dropdown for "Select the app" and "Select the device"
3. Select:
   - App: **Mail**
   - Device: **Windows Computer** (or your device type)
4. Click **Generate**
5. Google will show you a 16-character password like: `xhyw yenx ykyp ievw`
6. **Copy this exact password** (you can copy with or without spaces)

### Step 3: Update `.env` File
1. Open `O:\subscription_reminder\backend\.env`
2. Find the line: `SMTP_PASS=xhyw yenx ykyp ievw`
3. Replace it with your new 16-character App Password
4. Example:
   ```
   SMTP_PASS=abcd efgh ijkl mnop
   ```
5. Save the file

### Step 4: Restart the Backend
```powershell
# Kill any running python
taskkill /F /IM python.exe

# Start the backend server
cd O:\subscription_reminder
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### Step 5: Test SMTP
```powershell
# Login to get a token
$login = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/auth/login' `
  -ContentType 'application/json' `
  -Body (@{ email = 'e2e_abc123@example.com'; password = 'TestPass123!' } | ConvertTo-Json)
$token = $login.access_token

# Test SMTP
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/auth/test-smtp' `
  -Headers @{ Authorization = "Bearer $token" }
```

**Expected response:** `{"status":"success","message":"SMTP login successful"}`

### Step 6: Send Test Email
```powershell
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/auth/send-test-email' `
  -Headers @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" } `
  -Body (@{ subject = 'Test Email'; message = 'Hello! This is a test.' } | ConvertTo-Json)
```

**Expected response:** `{"status":"success","message":"Test email sent successfully to e2e_abc123@example.com"}`

## Troubleshooting

### If you still get 535 BadCredentials:
1. **Verify the exact password:** Copy it again from https://myaccount.google.com/apppasswords (passwords can be regenerated)
2. **Check 2FA is enabled:** Go to https://myaccount.google.com/security → "2-Step Verification" should show "On"
3. **Try a different app password:** Sometimes older ones are blocked. Generate a new one.
4. **Check account security:** If your Gmail account had suspicious activity, Google may block app passwords. Check https://myaccount.google.com/security-checkup

### If you don't see "App passwords" option:
1. 2-Step Verification must be enabled first
2. The account must have 2FA active
3. Note: App passwords don't work with regular Gmail passwords or Microsoft/Google-managed accounts

## Success Confirmation
Once SMTP is working:
- Users can send test emails from the application
- The scheduler will send subscription renewal reminders via email
- All E2E tests will pass
