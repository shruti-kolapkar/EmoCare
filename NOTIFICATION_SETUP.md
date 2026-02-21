# Notification System Setup Guide

This guide will help you configure email and SMS alerts for the Stress-Sync Pro system.

## 📧 Email Notifications (Gmail Setup)

### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification if not already enabled

### Step 2: Create App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Windows Computer" (or your device)
3. Google will generate a 16-character password
4. Copy this password

### Step 3: Update Your Code
In `app.py`, find the `send_email_alert()` function and update:

```python
sender_email = "your-email@gmail.com"  # Your Gmail address
sender_password = "xxxx xxxx xxxx xxxx"  # Paste the 16-char password here
```

### Step 4: Test Email
Run the app and set stress level above the alert threshold to trigger an email.

---

## 📱 SMS Notifications (Twilio Setup - Optional)

### Step 1: Create Twilio Account
1. Sign up at [Twilio.com](https://www.twilio.com/console)
2. Verify your phone number
3. Get your free trial phone number

### Step 2: Get Your Credentials
From Twilio Console:
- Account SID
- Auth Token
- Twilio Phone Number (assigned to you)

### Step 3: Install Twilio Package
```bash
pip install twilio
```

### Step 4: Enable SMS in Your Code
In `app.py`, find the `send_sms_alert()` function and uncomment:

```python
from twilio.rest import Client

account_sid = "your_account_sid"          # From Twilio
auth_token = "your_auth_token"            # From Twilio
client = Client(account_sid, auth_token)
message = client.messages.create(
    body=f"🚨 ALERT: Patient {patient_name} has HIGH STRESS level ({stress_level}%). Check immediately!",
    from_="+1234567890",                   # Your Twilio phone number
    to=nurse_phone                         # Recipient's phone
)
```

### Step 5: Test SMS
Run the app and enable SMS alerts in the sidebar to test.

---

## 🔧 Configuration Options in Dashboard

The sidebar now includes:

- **Patient Name**: Patient being monitored
- **Nurse Name**: Nurse/Caregiver name
- **Nurse Email**: Email for alerts
- **Nurse Phone**: Phone number for SMS (include country code)
- **Email Alerts**: Toggle email notifications on/off
- **SMS Alerts**: Toggle SMS notifications on/off
- **Alert Cooldown**: Minutes between repeated alerts (prevents spam)

---

## 📊 Alert Logs

Two log files are created automatically:

1. **nurse_alerts.log** - Detailed log of all stress alerts sent
2. **sms_alerts.log** - Log of SMS attempts

View these files to track alert history.

---

## ⚠️ Important Notes

- **Gmail**: Uses Gmail's SMTP server (secure connection on port 465)
- **SMS**: Requires Twilio account (free trial available, paid plans after)
- **Security**: Never commit your passwords/tokens to version control
- **Testing**: Start with alerts enabled and lower the stress threshold to test

---

## 🛠️ Troubleshooting

### Email not sending?
- ✓ Check sender_email and sender_password are correct
- ✓ Verify 2FA is enabled on Gmail
- ✓ Make sure you used App Password, not regular password
- ✓ Check internet connection

### SMS not sending?
- ✓ Verify Twilio credentials are correct
- ✓ Ensure phone numbers include country code (+91 for India)
- ✓ Check Twilio account has sufficient balance

### Alerts not triggering?
- ✓ Ensure "Enable Remote Alerts" is toggled ON
- ✓ Lower the "Stress Alert Threshold" to test
- ✓ Check alert cooldown period (default 5 minutes)

---

## 🔐 Security Best Practices

1. **Don't hardcode credentials** - Use environment variables instead:
   ```python
   import os
   sender_password = os.getenv("GMAIL_APP_PASSWORD")
   ```

2. **Use .env file**:
   ```bash
   pip install python-dotenv
   ```
   
   Create `.env`:
   ```
   GMAIL_EMAIL=your-email@gmail.com
   GMAIL_PASSWORD=xxxx xxxx xxxx xxxx
   TWILIO_SID=your_sid
   TWILIO_TOKEN=your_token
   ```

3. **Load in code**:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   sender_email = os.getenv("GMAIL_EMAIL")
   ```

---

## 📞 Support

For issues with:
- **Gmail**: Visit [Google Account Support](https://support.google.com)
- **Twilio**: Visit [Twilio Support](https://support.twilio.com)
- **App Issues**: Debug using the logs and dashboard notifications
