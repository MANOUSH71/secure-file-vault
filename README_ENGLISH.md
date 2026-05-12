# 🔐 Secure File Vault Pro

## Professional File Encryption & Sharing System

A complete web-based file encryption and sharing system with multiple encryption methods, secure file storage, and advanced features.

---

## ✅ Status: FULLY FUNCTIONAL

The application is running and ready to use!

**Access URL**: http://localhost:5000

---

## 🚀 Features

### Core Features
- ✅ **4 Encryption Methods**
  - AES-256-GCM (Advanced Encryption Standard)
  - ChaCha20-Poly1305 (Modern Stream Cipher)
  - Fernet (Symmetric Encryption)
  - RSA-2048 (Asymmetric Encryption)

- ✅ **File Management**
  - Upload & Encrypt files
  - Download & Decrypt files
  - Delete files
  - File preview (images & text)

- ✅ **Secure Sharing**
  - Generate expiring share links
  - Password-protected shares
  - Track share statistics

- ✅ **User Management**
  - User registration & login
  - Secure authentication
  - User profiles

### Professional Features
- ✅ **Email Integration** - Send encrypted files via email
- ✅ **File Preview** - Preview images and text files
- ✅ **Activity Logging** - Track all user activities
- ✅ **Two-Factor Authentication** - TOTP with QR codes
- ✅ **Modern UI** - Dark theme with gradient effects
- ✅ **Responsive Design** - Works on all devices

---

## 🎯 Quick Start

### 1. Start the Application
The server is already running on:
```
http://localhost:5000
```

### 2. Create an Account
1. Open http://localhost:5000
2. Click "Sign Up" tab
3. Fill in your details
4. Click "Create Account"

### 3. Login
1. Enter your username and password
2. Click "Login"

### 4. Encrypt Files
1. Drag & drop a file or click to select
2. Choose encryption method
3. Enter password
4. Click "Encrypt File"

### 5. Decrypt Files
1. Click "Decrypt" on any file
2. Enter password
3. Click "Decrypt & Download"

### 6. Share Files
1. Click "Share" on any file
2. Set expiry duration
3. Optional: Add share password
4. Click "Create Link"
5. Copy and share the link

---

## 📊 Encryption Methods

### 1. AES-256-GCM
- **Type**: Symmetric encryption
- **Key Size**: 256 bits
- **Best For**: General purpose, high security
- **Speed**: Very fast

### 2. ChaCha20-Poly1305
- **Type**: Stream cipher with authentication
- **Key Size**: 256 bits
- **Best For**: Mobile devices, high performance
- **Speed**: Extremely fast

### 3. Fernet
- **Type**: Symmetric encryption (AES-128-CBC + HMAC)
- **Key Size**: 128 bits
- **Best For**: Simple encryption needs
- **Speed**: Fast

### 4. RSA-2048
- **Type**: Asymmetric encryption
- **Key Size**: 2048 bits
- **Best For**: Small files, key exchange
- **Speed**: Slower (for small files only)

---

## 🔧 Technical Stack

### Backend
- **Flask** - Python web framework
- **SQLite** - Database
- **Cryptography** - Encryption library
- **Pillow** - Image processing
- **PyOTP** - Two-factor authentication
- **QRCode** - QR code generation

### Frontend
- **Bootstrap 5** - UI framework
- **Font Awesome** - Icons
- **JavaScript** - Interactivity

---

## 📁 Project Structure

```
project/
├── app.py                      # Main application
├── models.py                   # Database models
├── crypto_manager.py           # Encryption methods
├── email_sender.py             # Email functionality
├── file_preview.py             # File preview
├── activity_logger.py          # Activity tracking
├── two_factor_auth.py          # 2FA implementation
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
├── vault.db                    # SQLite database
├── templates/
│   ├── index.html             # Login page (English)
│   └── dashboard_english.html # Dashboard (English)
├── static/
│   ├── css/                   # Stylesheets
│   └── js/                    # JavaScript files
└── uploads/                   # Encrypted files storage
```

---

## 🎨 User Interface

### Login Page
- Modern dark theme
- Gradient effects
- Password strength indicator
- Responsive design

### Dashboard
- File statistics
- Drag & drop upload
- File list with actions
- Encryption method badges
- Modal dialogs for decrypt/share

---

## 🔒 Security Features

### Encryption
- Multiple encryption algorithms
- Secure key derivation (PBKDF2)
- Random salt generation
- Authenticated encryption (GCM, Poly1305)

### Authentication
- Password hashing (Werkzeug)
- Session management
- Login required decorators
- Secure cookie handling

### File Storage
- Encrypted file storage
- Unique file IDs (UUID)
- Secure file deletion
- Access control

### Sharing
- Expiring share links
- Password-protected shares
- One-time download links
- Share tracking

---

## 📈 Statistics

- **Total Files**: Track encrypted files
- **Storage Size**: Monitor storage usage
- **Shares**: Count active shares

---

## 🎯 Use Cases

### Personal Use
- Encrypt sensitive documents
- Secure photo storage
- Password-protected file sharing

### Business Use
- Secure file transfer
- Client file sharing
- Document encryption
- Compliance requirements

### Development
- API integration
- Custom encryption workflows
- Automated file processing

---

## 🚀 Commands

### Start Server
```bash
python app.py
```

### Access Application
```
http://localhost:5000
```

### Stop Server
Press `Ctrl+C` in terminal

---

## 📞 Support

### Documentation
- README.md - Project overview
- Code comments - Inline documentation

### Test Credentials
Create your own account through the registration page!

---

## 🎉 Success!

Your **Secure File Vault Pro** is now running with:
- ✅ Full English interface
- ✅ 4 encryption methods
- ✅ File sharing system
- ✅ Professional features
- ✅ Modern UI/UX

**Enjoy your secure file vault!** 🔐

---

**Version**: 1.0.0  
**Language**: English  
**Status**: Production Ready  
**License**: MIT
