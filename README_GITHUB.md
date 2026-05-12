# 🔐 Secure File Vault Pro - Team Edition

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)

**Professional file encryption and team collaboration platform**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Security](#-security)

</div>

---

## 📖 Overview

**Secure File Vault Pro** is a comprehensive web-based file encryption and team collaboration platform built with Flask. It provides military-grade encryption with multiple algorithms, team management, real-time notifications, analytics, and much more.

### ✨ Key Highlights

- 🔒 **4 Encryption Methods**: AES-256-GCM, ChaCha20-Poly1305, Fernet, RSA-2048
- 👥 **Team Collaboration**: Up to 8 members per team with role-based access
- 📊 **Analytics Dashboard**: Real-time charts and statistics
- 🔔 **Notifications System**: In-app notifications with unread badges
- 🛡️ **2FA Authentication**: TOTP-based two-factor authentication
- 📋 **Audit Logging**: Complete activity tracking with IP addresses
- 📤 **Public File Requests**: Allow anyone to upload files without an account
- 🎨 **Modern UI**: Dark theme with responsive Bootstrap 5 design

---

## 🎯 Features

### Core Features
- ✅ **File Encryption/Decryption** with 4 different algorithms
- ✅ **Secure File Sharing** with expiring links and passwords
- ✅ **User Authentication** with session management
- ✅ **File Statistics** and usage tracking

### Team Features (15 Advanced Features)
1. **Teams & Workspaces** - Create teams with role-based access (admin, editor, viewer)
2. **Shared Folders** - Organize files in folders with per-member permissions
3. **Member Invitations** - Invite users via email or one-time links
4. **Team Activity Feed** - Real-time activity tracking
5. **Admin Panel** - User management, deactivation, link revocation
6. **Analytics Dashboard** - Charts with Chart.js (files over time, encryption breakdown, storage per member)
7. **File Requests** - Generate public upload links for non-users
8. **Audit Log** - Tamper-evident logging with IP tracking
9. **2FA Enforcement** - Team-level 2FA requirements
10. **File Expiry** - Automatic file deletion after expiry
11. **Session Management** - View and revoke active sessions
12. **Tags & Search** - Tag files and advanced search functionality
13. **Bulk Operations** - Select multiple files for batch actions
14. **Notifications Center** - In-app notifications with bell icon
15. **Profile & Settings** - Complete user profile management

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/secure-file-vault-pro.git
cd secure-file-vault-pro
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Open your browser:**
```
http://localhost:5000
```

That's it! 🎉

---

## 📦 Dependencies

```
Flask==3.0.0
Flask-CORS==4.0.0
cryptography==41.0.7
Werkzeug==3.0.1
Pillow==10.1.0
pyotp==2.9.0
qrcode==7.4.2
```

---

## 💻 Usage

### For Solo Users

1. **Register an account**
2. **Upload and encrypt files** with your preferred encryption method
3. **Create share links** with expiry dates and passwords
4. **Download and decrypt** files anytime

### For Teams

1. **Create a team** from the Teams page
2. **Invite members** using invitation links
3. **Assign roles** (admin, editor, viewer)
4. **Share files** within the team
5. **Monitor activity** in the activity feed
6. **View analytics** in the analytics dashboard

### For File Collection

1. **Create a file request** from the File Request page
2. **Share the upload link** with anyone
3. **Receive notifications** when files are uploaded
4. **Files are automatically encrypted** on arrival

---

## 🔐 Security

### Encryption Algorithms

- **AES-256-GCM**: Advanced Encryption Standard with Galois/Counter Mode
- **ChaCha20-Poly1305**: Modern stream cipher with authentication
- **Fernet**: Symmetric encryption with built-in authentication
- **RSA-2048**: Asymmetric encryption for small files

### Security Features

- ✅ Password hashing with Werkzeug
- ✅ TOTP-based 2FA with QR codes
- ✅ Session management and revocation
- ✅ Audit logging with IP tracking
- ✅ CSRF protection
- ✅ Secure file upload with size limits
- ✅ Expiring share links
- ✅ Password-protected shares

---

## 📊 Architecture

### Backend
- **Framework**: Flask 3.0.0
- **Database**: SQLite with 16 tables
- **Authentication**: Session-based with 2FA support
- **Encryption**: cryptography library

### Frontend
- **Framework**: Bootstrap 5
- **Icons**: Font Awesome 6.4.0
- **Charts**: Chart.js 4.4.0
- **Theme**: Custom dark theme with purple/teal gradients

### Database Schema
- 16 tables including users, files, teams, notifications, audit logs, etc.
- 50+ database methods for all operations
- Complete relational integrity

---

## 📁 Project Structure

```
secure-file-vault-pro/
├── app.py                      # Main Flask application
├── models.py                   # Database models and methods
├── crypto_manager.py           # Encryption/decryption logic
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── templates/                  # Jinja2 templates
│   ├── index.html             # Login/Register page
│   ├── dashboard_english.html # Main dashboard
│   ├── team.html              # Team management
│   ├── notifications.html     # Notifications center
│   ├── settings.html          # User settings
│   ├── analytics.html         # Analytics dashboard
│   ├── file_request.html      # File request creation
│   ├── upload.html            # Public upload page
│   ├── audit.html             # Audit log viewer
│   ├── admin.html             # Admin panel
│   ├── team_activity.html     # Team activity feed
│   ├── invitation.html        # Team invitation page
│   ├── share.html             # Share link viewer
│   └── error.html             # Error page
├── uploads/                    # Encrypted files storage
├── static/                     # Static assets
│   ├── css/
│   └── js/
└── docs/                       # Documentation
    ├── FEATURES_GUIDE.md
    ├── IMPLEMENTATION_COMPLETE.md
    └── QUICK_START_TEAM.md
```

---

## 🎨 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

### Team Management
![Teams](https://via.placeholder.com/800x400?text=Team+Management+Screenshot)

### Analytics
![Analytics](https://via.placeholder.com/800x400?text=Analytics+Dashboard+Screenshot)

---

## 📚 Documentation

- **[Features Guide](FEATURES_GUIDE.md)** - Detailed documentation of all 15 features
- **[Implementation Guide](IMPLEMENTATION_COMPLETE.md)** - Technical implementation details
- **[Quick Start Guide](QUICK_START_TEAM.md)** - Get started in 5 minutes
- **[Arabic Guide](README_ENGLISH.md)** - دليل باللغة العربية

---

## 🛣️ Roadmap

### Completed ✅
- [x] Core encryption/decryption
- [x] User authentication
- [x] File sharing
- [x] Team management
- [x] Analytics dashboard
- [x] Notifications system
- [x] 2FA authentication
- [x] Audit logging
- [x] File requests
- [x] Session management

### Planned 🚧
- [ ] Real-time notifications with WebSockets
- [ ] File versioning
- [ ] Collaborative editing
- [ ] Mobile app
- [ ] Desktop client
- [ ] Cloud storage integration (S3, Azure)
- [ ] LDAP/SSO integration
- [ ] Compliance reports (GDPR, HIPAA)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Flask framework and community
- Bootstrap for the UI framework
- Chart.js for beautiful charts
- Font Awesome for icons
- cryptography library for encryption

---

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Contact via email

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ and Python**

[⬆ Back to Top](#-secure-file-vault-pro---team-edition)

</div>
