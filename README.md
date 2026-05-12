# 🔐 Secure File Vault Pro - Client-Side Encryption

## Pure Client-Side File Encryption Application

A complete client-side web application for encrypting and managing files with military-grade security. No server required - everything runs in your browser!

---

## ✨ Features

### 🔒 Encryption
- **AES-256-GCM**: Industry standard encryption (Recommended)
- **AES-256-CBC**: High compatibility mode
- **AES-256-CTR**: Fast streaming encryption
- **ChaCha20-Poly1305**: Modern alternative for mobile
- **Client-Side Only**: All encryption happens in your browser
- **Zero-Knowledge**: Your files never leave your device unencrypted

### 💾 File Management
- Upload and encrypt files (up to 100MB)
- Decrypt and download files
- Delete files securely
- Real-time file search
- Detailed file statistics dashboard

### 🔗 Secure Sharing
- Create unique shareable links
- Set expiration time for links
- Optional password protection for shares
- Global sharing support via **Cloud Integration (Firebase)**

### 🎨 Modern UI/UX
- Beautiful dark gradient design
- Drag & drop file upload
- Fully responsive (Mobile friendly)
- Real-time activity notifications
- Detailed audit logs for security tracking

---

## 📋 Requirements

- **Modern Web Browser** (Chrome, Firefox, Edge, Safari)
- **JavaScript Enabled**
- **LocalStorage Support**

---

## 🚀 Quick Start

1. **Open the App**: Double-click `index.html` or drag it into your browser.
2. **Create Account**: All data is stored locally in your browser or synced to your cloud.
3. **Encrypt Files**: Choose a file, select encryption method, set a password, and click Encrypt.
4. **Share Globally**: Go to **Settings**, connect your **Firebase** config, and your share links will work for anyone!

---

## 🔧 Technical Details

### Security Architecture
- **Key Derivation**: PBKDF2 with 100,000 iterations and random salt.
- **Hashing**: SHA-256 for secure password storage.
- **Storage**: Browser's LocalStorage for local use, Firebase for global sharing.

### Browser Compatibility
| Browser | Version | Support |
|---------|---------|---------|
| Chrome  | 60+     | ✅ Full |
| Firefox | 55+     | ✅ Full |
| Safari  | 11+     | ✅ Full |
| Edge    | 79+     | ✅ Full |

---

## 🛡️ Security Best Practices

1. **Strong Passwords**: Use at least 12 characters with a mix of symbols and numbers.
2. **Extra Keys**: For highly sensitive files, use the "Additional Key" feature.
3. **Link Expiry**: Set the shortest possible expiration time for shared links.
4. **Firebase Rules**: If using Cloud Integration, ensure your Firebase security rules are properly configured.

---

## 📁 Project Structure

```
secure-vault/
├── index.html          # Main application interface
├── share.html          # Shared file access page
├── styles.css          # Modern UI styling
├── app.js              # Core application logic
├── crypto.js           # Advanced encryption engine
├── cloud.js            # Firebase cloud integration
├── settings.js         # User settings and cloud config
├── analytics.js        # Statistics and charts
├── notifications.js    # User alert system
├── audit.js            # Security activity tracking
└── requests.js         # File request system
```

---

## 🌐 Hosting

You can host this project for free on:
- **GitHub Pages**
- **Netlify**
- **Vercel**

Since it's a pure client-side app, it requires **zero server-side configuration**.

---

## ⚠️ Disclaimer

- This application is for educational and personal privacy purposes.
- **Lost passwords cannot be recovered.**
- Always maintain backups of your important files.
- Use at your own risk.

---

## 📜 License

Open source and free for personal and commercial use.

---

**Made with ❤️ for Privacy and Security**

**Version**: 1.1.0  
**Last Updated**: 2026  
**Status**: Production Ready ✅
