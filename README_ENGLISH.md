# 🔐 Secure File Vault Pro - Web Application

An advanced web application for encrypting and managing files with high security, supporting multiple encryption methods and a secure sharing system.

## ✨ Features

### 🔒 Multiple Encryption Methods
- **AES-256-GCM**: Industry standard, fast and secure (recommended)
- **ChaCha20-Poly1305**: Modern alternative to AES, excellent for mobile devices
- **Fernet**: Simple and secure, built on AES-128
- **RSA-2048**: Asymmetric encryption, ideal for small files

### 📤 Sharing System
- Create secure sharing links
- Set link expiration time
- Password-protect links
- Track download counts

### 💾 File Management
- Upload and encrypt files (up to 100MB)
- Direct decryption and download
- Delete files
- View detailed statistics

### 🎨 Modern User Interface
- Attractive Dark Mode design
- Full Arabic interface (RTL support)
- Drag & Drop for files
- Responsive Design

### 🔐 Security
- Military-grade strong encryption
- PBKDF2 for key derivation (100,000 iterations)
- Data compression before encryption
- Zero-Knowledge Architecture

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Web browser (Chrome, Firefox, Edge, Safari)

## 🚀 Installation and Setup

### Step 1: Download the Project

#### Option A: Download ZIP File
1. Download the project as a ZIP file
2. Extract the ZIP file to your desired location (e.g., `C:\Projects\secure-vault-web`)
3. Open the extracted folder

#### Option B: Clone from Git (if available)
```bash
git clone <repository-url>
cd secure-vault-web
```

### Step 2: Install Python

If you don't have Python installed:

1. Visit [python.org](https://www.python.org/downloads/)
2. Download Python 3.8 or higher
3. **Important**: During installation, check "Add Python to PATH"
4. Complete the installation

To verify Python is installed:
```bash
python --version
```

### Step 3: Open Command Prompt in Project Folder

#### Method 1: Using File Explorer
1. Open the project folder in File Explorer
2. Hold `Shift` and right-click in the empty space
3. Select "Open PowerShell window here" or "Open Command Prompt here"

#### Method 2: Using Command Prompt
```bash
cd "e:\project shreef 3"
```

### Step 4: Install Required Libraries

Run this command in the terminal:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- cryptography (encryption library)
- Werkzeug (security utilities)

### Step 5: Run the Application

Start the application with:

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.x:5000
```

### Step 6: Open in Browser

1. Open your web browser
2. Go to: `http://localhost:5000`
3. The application should load successfully

## 📁 Project Structure

```
secure-vault-web/
├── app.py                 # Flask main application
├── crypto_manager.py      # All encryption methods
├── models.py              # SQLite database
├── config.py              # Configuration settings
├── email_sender.py        # Email functionality
├── file_preview.py        # File preview features
├── activity_logger.py     # Activity logging
├── requirements.txt       # Required libraries
├── README.md             # Arabic documentation
├── README_ENGLISH.md     # This file
├── run.bat               # Windows batch file to run app
├── vault.db              # Database (created automatically)
├── uploads/              # Encrypted files folder
├── templates/            # HTML templates
│   ├── index.html       # Login page
│   ├── dashboard.html   # Dashboard
│   ├── share.html       # Sharing page
│   └── error.html       # Error page
└── static/              # CSS/JS files
    ├── css/
    └── js/
```

## 🎯 How to Use

### 1. Create an Account

1. Open the application
2. Click "Create Account"
3. Enter your details:
   - Username
   - Email
   - Password (strong password recommended)
4. Click "Register"

### 2. Encrypt a File

1. **Upload File**:
   - Drag and drop a file into the upload area, OR
   - Click the upload area to browse and select a file
   
2. **Choose Encryption Method**:
   - **AES-256-GCM**: Best for most cases (recommended)
   - **ChaCha20-Poly1305**: Good for mobile devices
   - **Fernet**: Simple and reliable
   - **RSA-2048**: For small files only

3. **Set Password**:
   - Enter a strong password (12+ characters)
   - Use mix of uppercase, lowercase, numbers, and symbols
   
4. **Optional - Additional Key**:
   - Add an extra security layer
   - Keep this key safe - you'll need it to decrypt

5. **Click "Encrypt File"**
   - File will be encrypted and saved
   - Original file is not stored

### 3. Decrypt a File

1. Find your file in the dashboard
2. Click "Decrypt" button next to the file
3. Enter the password and additional key (if used)
4. Click "Decrypt"
5. The original file will download automatically

### 4. Share a File

1. Click "Share" button next to the file
2. Set sharing options:
   - **Expiration Time**: How long the link stays valid
   - **Password Protection**: Optional password for the link
   - **Download Limit**: Maximum number of downloads
3. Click "Create Share Link"
4. Copy the link and share it securely

### 5. Access Shared File

1. Open the shared link in browser
2. Enter password if required
3. Click "Download"
4. File will be decrypted and downloaded

## 🔧 Advanced Configuration

### Change Maximum File Size

Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### Change PBKDF2 Iterations

Edit `crypto_manager.py`:
```python
self.iterations = 100_000  # Increase for higher security
```

### Change Server Port

Edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port number
```

### Enable Email Notifications

Edit `config.py`:
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

## 🛡️ Security Best Practices

### 1. Strong Passwords
- Use at least 12 characters
- Mix uppercase and lowercase letters
- Include numbers and special symbols
- Avoid common words or patterns
- Example: `MyV@ult2024!Secure#`

### 2. Additional Key
- Adds an extra security layer
- Store it separately from your password
- Never share it with anyone
- Keep a backup in a secure location

### 3. Backup Your Data
- Regularly backup `vault.db` file
- Store backups in a secure location
- Test your backups periodically

### 4. Production Deployment
- Always use HTTPS in production
- Use environment variables for secrets
- Enable firewall rules
- Regular security updates

### 5. File Recovery
- **Important**: Files cannot be recovered without the correct password
- There is no "forgot password" option for encrypted files
- Keep your passwords safe and backed up

## 🚨 Troubleshooting

### Application Won't Start

**Problem**: `ModuleNotFoundError: No module named 'flask'`
**Solution**: Install requirements again
```bash
pip install -r requirements.txt
```

**Problem**: `Port 5000 is already in use`
**Solution**: Change port in `app.py` or stop other application using port 5000

### Can't Access from Browser

**Problem**: Browser shows "Can't reach this page"
**Solution**: 
1. Check if application is running in terminal
2. Try `http://127.0.0.1:5000` instead of `localhost`
3. Check firewall settings

### File Upload Fails

**Problem**: "File too large" error
**Solution**: Check file size limit in `app.py` and increase if needed

**Problem**: "Invalid file type"
**Solution**: Check allowed file extensions in configuration

### Decryption Fails

**Problem**: "Decryption failed" error
**Solution**: 
1. Verify password is correct
2. Check if additional key was used during encryption
3. Ensure file hasn't been corrupted

## 🌟 Upcoming Features

- [ ] Email file sending
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] Full folder encryption
- [ ] Mobile application
- [ ] Two-factor authentication (2FA)
- [ ] End-to-end encryption for sharing
- [ ] File versioning
- [ ] Batch file operations
- [ ] API for third-party integration

## 💡 Tips and Tricks

### Quick Start with Batch File

Create `run.bat` in project folder:
```batch
@echo off
echo Starting Secure File Vault Pro...
python app.py
pause
```

Double-click `run.bat` to start the application quickly.

### Access from Other Devices

To access from other devices on your network:
1. Find your computer's IP address:
   ```bash
   ipconfig
   ```
2. Look for "IPv4 Address" (e.g., 192.168.1.100)
3. On other device, open: `http://192.168.1.100:5000`

### Keyboard Shortcuts

- `Ctrl + U`: Focus on upload area
- `Ctrl + F`: Search files
- `Esc`: Close modals
- `Enter`: Submit forms

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📧 Support

For questions and support:
- Open an issue in the project
- Check documentation
- Review troubleshooting section

## ⚠️ Disclaimer

This application is for educational purposes. For production use, a comprehensive security audit is recommended.

---

**Made with ❤️ in Egypt 🇪🇬**

## 🎓 Learning Resources

### Understanding Encryption
- [AES Encryption Explained](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [Public Key Cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography)

### Python & Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Cryptography Library](https://cryptography.io/)

### Security Best Practices
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Password Security Guidelines](https://pages.nist.gov/800-63-3/)

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Active Development
