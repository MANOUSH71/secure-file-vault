# 🚀 Quick Start Guide - Team Edition

## Get Started in 5 Minutes!

### Step 1: Start the Server
```bash
cd "e:\project shreef 3"
python app.py
```

### Step 2: Open Browser
Navigate to: **http://localhost:5000**

### Step 3: Create Account
1. Click "Register"
2. Fill in your details
3. Click "Create Account"

---

## 🎯 Quick Feature Tour

### 1️⃣ Upload Your First File (30 seconds)
1. On dashboard, drag a file to the upload zone
2. Choose encryption method (AES recommended)
3. Enter a password
4. Click "Encrypt File"
5. ✅ Done! Your file is encrypted and stored

### 2️⃣ Create Your First Team (1 minute)
1. Click "Teams" in navbar
2. Click "Create Team"
3. Enter team name (e.g., "My Team")
4. Click "Create"
5. ✅ You're now a team owner!

### 3️⃣ Invite Team Members (1 minute)
1. On team page, click "View" on your team
2. Click "Invite Member"
3. Click "Generate Invite"
4. Copy the link
5. Share with your team members
6. ✅ They can now join your team!

### 4️⃣ Create File Request (1 minute)
1. Click "File Request" in navbar
2. Set max files (e.g., 5)
3. Set expiry (e.g., 48 hours)
4. Click "Generate Upload Link"
5. Copy and share the link
6. ✅ Anyone can upload files to you!

### 5️⃣ Enable 2FA (2 minutes)
1. Click "Settings" in navbar
2. Scroll to "Two-Factor Authentication"
3. Click "Enable 2FA"
4. Scan QR code with Google Authenticator
5. ✅ Your account is now extra secure!

---

## 📱 Navigation Guide

### Main Menu:
- **Dashboard** - Upload, encrypt, decrypt files
- **Teams** - Manage teams and members
- **File Request** - Create public upload links
- **Audit** - View activity logs
- **🔔 Bell Icon** - Notifications (shows unread count)
- **Settings** - Profile, password, 2FA, sessions

### Team Menu (when viewing a team):
- **View** - See team members
- **Activity** - View team activity feed
- **Admin** - Admin panel (admin only)
- **Analytics** - View charts and stats (admin only)

---

## 🎨 Key Features at a Glance

### For Solo Users:
- ✅ Encrypt files with 4 methods
- ✅ Create expiring share links
- ✅ Password-protect shares
- ✅ Track file statistics
- ✅ Enable 2FA

### For Teams:
- ✅ Create teams (up to 8 members)
- ✅ Assign roles (admin, editor, viewer)
- ✅ Invite members via link
- ✅ View team activity feed
- ✅ Analytics dashboard
- ✅ Admin panel
- ✅ File requests (public upload)
- ✅ Audit logging
- ✅ Notifications

---

## 🔐 Security Tips

1. **Use strong passwords** - Mix letters, numbers, symbols
2. **Enable 2FA** - Extra layer of security
3. **Don't share passwords** - Use share links instead
4. **Set expiry dates** - Share links should expire
5. **Review sessions** - Check active sessions regularly
6. **Check audit log** - Monitor account activity

---

## 💡 Pro Tips

1. **Encryption Methods:**
   - **AES-256-GCM** - Best for most files (fast & secure)
   - **ChaCha20** - Great for mobile devices
   - **Fernet** - Simple and reliable
   - **RSA-2048** - Best for small files

2. **Team Roles:**
   - **Admin** - Full control (invite, remove, settings)
   - **Editor** - Can upload and share files
   - **Viewer** - Can only view files

3. **File Requests:**
   - Perfect for collecting files from clients
   - No account needed for uploaders
   - Files auto-encrypted on arrival

4. **Notifications:**
   - Get notified when files are shared with you
   - Get notified when someone uploads to your request
   - Get notified when invited to teams

---

## 🆘 Troubleshooting

### Server won't start?
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process if needed
taskkill /PID <process_id> /F

# Restart server
python app.py
```

### Can't login?
- Check username and password
- Try registering a new account
- Check if database file exists: `vault.db`

### Files not uploading?
- Check file size (max 100MB)
- Check if uploads folder exists
- Check browser console for errors

### 2FA not working?
- Make sure time is synced on your device
- Try regenerating the QR code
- Use the secret key manually if QR doesn't work

---

## 📚 Learn More

- **Full Features Guide:** See `FEATURES_GUIDE.md`
- **Implementation Details:** See `IMPLEMENTATION_COMPLETE.md`
- **Original README:** See `README_ENGLISH.md`

---

## 🎉 You're All Set!

Start encrypting files and collaborating with your team!

**Need help?** Check the documentation files or the audit log for troubleshooting.

---

**Happy Encrypting! 🔐**
