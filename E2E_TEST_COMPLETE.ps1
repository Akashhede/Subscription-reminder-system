# ============================================
# END-TO-END TEST SCRIPT
# ============================================
# This script tests the entire Subscription Reminder application
# Requirements: Backend must be running on http://127.0.0.1:8000

$API = "http://127.0.0.1:8000"
$PASSED = 0
$FAILED = 0

function Print-Test {
    param($title, $result)
    if ($result) {
        Write-Host "✓ $title" -ForegroundColor Green
        $script:PASSED++
    } else {
        Write-Host "✗ $title" -ForegroundColor Red
        $script:FAILED++
    }
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   SUBSCRIPTION REMINDER - E2E TEST" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Test 1: Backend is running
Write-Host "`n[TEST 1] Backend Connectivity" -ForegroundColor Yellow
try {
    $root = Invoke-RestMethod -Uri "$API/" -ErrorAction Stop
    Print-Test "Backend responds to root endpoint" ($root.msg -eq "Subscription Reminder API running")
} catch {
    Print-Test "Backend responds to root endpoint" $false
}

# Test 2: User Registration
Write-Host "`n[TEST 2] User Registration" -ForegroundColor Yellow
$email = "test_" + (Get-Random) + "@example.com"
$password = "SecurePass123!"
$phone = "5551234567"

try {
    $regBody = @{ email = $email; password = $password; phone = $phone } | ConvertTo-Json
    $reg = Invoke-RestMethod -Method Post -Uri "$API/auth/register" -ContentType 'application/json' -Body $regBody -ErrorAction Stop
    Print-Test "User registration succeeds" ($reg.email -eq $email)
    Print-Test "User has ID" ($reg.id -gt 0)
    $userId = $reg.id
} catch {
    Print-Test "User registration succeeds" $false
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# Test 3: User Login
Write-Host "`n[TEST 3] User Authentication" -ForegroundColor Yellow
try {
    $loginBody = @{ email = $email; password = $password } | ConvertTo-Json
    $login = Invoke-RestMethod -Method Post -Uri "$API/auth/login" -ContentType 'application/json' -Body $loginBody -ErrorAction Stop
    Print-Test "Login succeeds" ($login.access_token -ne $null)
    Print-Test "Token is JWT format" ($login.access_token.Split('.').Length -eq 3)
    $token = $login.access_token
} catch {
    Print-Test "Login succeeds" $false
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Gray
    exit 1
}

# Test 4: JWT Token Validation
Write-Host "`n[TEST 4] Token Validation" -ForegroundColor Yellow
try {
    $debug = Invoke-RestMethod -Method Get -Uri "$API/auth/debug-token" `
        -Headers @{ Authorization = "Bearer $token" } -ErrorAction Stop
    Print-Test "Token can be decoded" ($debug.payload -ne $null)
    Print-Test "Token contains user_id" ($debug.payload.user_id -eq $userId)
    Print-Test "Token has expiration" ($debug.payload.exp -gt 0)
} catch {
    Print-Test "Token can be decoded" $false
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# Test 5: Get User Profile
Write-Host "`n[TEST 5] User Profile" -ForegroundColor Yellow
try {
    $profile = Invoke-RestMethod -Method Get -Uri "$API/auth/profile" `
        -Headers @{ Authorization = "Bearer $token" } -ErrorAction Stop
    Print-Test "Get profile succeeds" ($profile.email -eq $email)
    Print-Test "Profile has email alerts field" ($profile.email_alerts_enabled -ne $null)
} catch {
    Print-Test "Get profile succeeds" $false
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# Test 6: Update Email Preferences
Write-Host "`n[TEST 6] Email Preferences" -ForegroundColor Yellow
try {
    $prefBody = @{ email_alerts_enabled = $true } | ConvertTo-Json
    $prefRes = Invoke-RestMethod -Method Put -Uri "$API/auth/profile" `
        -Headers @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" } `
        -Body $prefBody -ErrorAction Stop
    Print-Test "Enable email alerts succeeds" ($prefRes.email_alerts_enabled -eq $true)
} catch {
    Print-Test "Enable email alerts succeeds" $false
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# Test 7: SMTP Configuration Test
Write-Host "`n[TEST 7] SMTP Configuration" -ForegroundColor Yellow
try {
    $smtpRes = Invoke-RestMethod -Method Post -Uri "$API/auth/test-smtp" `
        -Headers @{ Authorization = "Bearer $token" } -ErrorAction Stop
    Print-Test "SMTP login succeeds" ($smtpRes.status -eq "success")
    Print-Test "SMTP server responds" ($smtpRes.message -like "*SMTP login successful*")
} catch {
    Print-Test "SMTP login succeeds" $false
    $errMsg = $_.Exception.Response.Content.ReadAsStringAsync().Result
    if ($errMsg -like "*BadCredentials*") {
        Write-Host "  SMTP Issue: Gmail App Password is invalid" -ForegroundColor Yellow
        Write-Host "  Action: See GMAIL_APP_PASSWORD_FIX.md for instructions" -ForegroundColor Yellow
    } else {
        Write-Host "  Error: $errMsg" -ForegroundColor Gray
    }
}

# Test 8: Send Test Email
Write-Host "`n[TEST 8] Email Sending" -ForegroundColor Yellow
try {
    $emailBody = @{
        subject = "E2E Test Email"
        message = "This is an automated test email from Subscription Reminder application."
    } | ConvertTo-Json
    $emailRes = Invoke-RestMethod -Method Post -Uri "$API/auth/send-test-email" `
        -Headers @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" } `
        -Body $emailBody -ErrorAction Stop
    Print-Test "Send test email succeeds" ($emailRes.status -eq "success")
    Print-Test "Email delivered to user" ($emailRes.message -like "*sent successfully*")
} catch {
    Print-Test "Send test email succeeds" $false
    $errMsg = $_.Exception.Response.Content.ReadAsStringAsync().Result
    if ($errMsg -like "*BadCredentials*" -or $errMsg -like "*SMTP*") {
        Write-Host "  SMTP Issue: Check Gmail App Password" -ForegroundColor Yellow
    } else {
        Write-Host "  Error: $errMsg" -ForegroundColor Gray
    }
}

# Test 9: Create Subscription (if subscription routes exist)
Write-Host "`n[TEST 9] Subscription Management" -ForegroundColor Yellow
try {
    $subBody = @{
        name = "Netflix"
        renewal_date = (Get-Date).AddMonths(1).ToString("yyyy-MM-dd")
        cost = 15.99
        note = "Test subscription"
    } | ConvertTo-Json
    $subRes = Invoke-RestMethod -Method Post -Uri "$API/subscription/add" `
        -Headers @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" } `
        -Body $subBody -ErrorAction Stop
    Print-Test "Add subscription succeeds" ($subRes.id -gt 0)
    Print-Test "Subscription has correct name" ($subRes.name -eq "Netflix")
} catch {
    Print-Test "Add subscription succeeds" $false
    Write-Host "  Error: May not be implemented or endpoint issue" -ForegroundColor Gray
}

# Summary
Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "   TEST RESULTS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✓ Passed: $PASSED" -ForegroundColor Green
Write-Host "✗ Failed: $FAILED" -ForegroundColor $(if ($FAILED -gt 0) { "Red" } else { "Green" })

if ($FAILED -eq 0) {
    Write-Host "`n✓ ALL TESTS PASSED!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n⚠ Some tests failed. Review the output above." -ForegroundColor Yellow
    exit 1
}
