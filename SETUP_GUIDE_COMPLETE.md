# 🔐 Complete Setup Guide - Secure File Vault Pro

## Two Versions Available

Your Secure File Vault Pro comes in **two versions**:

1. **Python/Flask Version** (Backend + Frontend)
2. **HTML/CSS/JavaScript Version** (Pure Frontend)

---

## 📊 Version Comparison

| Feature | Python Version | HTML Version |
|---------|---------------|--------------|
| **Installation** | Requires Python | No installation |
| **Server** | Needs Flask server | No server needed |
| **Storage** | SQLite database | Browser LocalStorage |
| **File Size** | Up to 100MB+ | Up to 5-10MB |
| **Sharing** | Full featured | Basic sharing |
| **Multi-user** | Full support | Browser-based |
| **Deployment** | Needs hosting | Static hosting |
| **Security** | Server-side | Client-side |
| **Best For** | Teams, Production | Personal, Quick use |

---

## 🚀 Option 1: Python/Flask Version

### Requirements
- Python 3.8+
- pip
- 500MB disk space

### Installation Steps

#### 1. Install Python
1. Download from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH"
3. Install

#### 2. Open Terminal in Project Folder
**Windows**:
- Hold `Shift` + Right-click in folder
- Select "Open PowerShell here"

**Mac/Linux**:
```bash
cd /path/to/project
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- cryptography (encryption)
- Werkzeug (security)

#### 4. Run Application
```bash
python app.py
```

#### 5. Open Browser
Go to: `http://localhost:5000`

### Quick Run (Windows)
Double-click `run.bat` file

### Features Available
✅ Multiple users with authentication  
✅ SQLite database storage  
✅ Unlimited file size (configurable)  
✅ Team management  
✅ Advanced sharing  
✅ Email notifications  
✅ Audit logs  
✅ Analytics  
✅ File requests  
✅ Admin panel  

---

## 🌐 Option 2: HTML/CSS/JavaScript Version

### Requirements
- Modern web browser
- That's it!

### Installation Steps

#### 1. Download Files
Get these 5 files:
- `index.html`
- `share.html`
- `styles.css`
- `crypto.js`
- `app.js`

#### 2. Open Application
**Method 1**: Double-click `index.html`

**Method 2**: Drag `index.html` into browser

**Method 3**: Right-click → Open With → Browser

#### 3. Start Using
No installation, no setup, just works!

### Features Available
✅ Client-side encryption  
✅ Multiple accounts (browser-based)  
✅ File management  
✅ Basic sharing  
✅ Search & filter  
✅ Drag & drop  
✅ Mobile responsive  
✅ No server needed  

---

## 🎯 Which Version Should I Use?

### Choose Python Version If:
- ✅ You need multi-user support
- ✅ You want team collaboration
- ✅ You need large file support (100MB+)
- ✅ You want advanced features
- ✅ You can install Python
- ✅ You need production deployment

### Choose HTML Version If:
- ✅ You want instant setup (no installation)
- ✅ You need personal use only
- ✅ You want maximum privacy (no server)
- ✅ You have small files (<10MB)
- ✅ You want to host on GitHub Pages
- ✅ You want offline capability

---

## 📁 Project Structure

### Python Version Files
```
project/
├── app.py                    # Main Flask application
├── crypto_manager.py         # Encryption functions
├── models.py                 # Database models
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── run.bat                   # Quick start (Windows)
├── vault.db                  # Database (auto-created)
├── uploads/                  # Encrypted files
└── templates/                # HTML templates
    ├── index.html           # Login page
    ├── dashboard.html       # Main dashboard
    ├── share.html           # Share page
    └── ...
```

### HTML Version Files
```
project/
├── index.html               # Main application
├── share.html               # Shared file access
├── styles.css               # All styles
├── crypto.js                # Encryption library
└── app.js                   # Application logic
```

---

## 🔧 Configuration

### Python Version

#### Change Port
Edit `app.py`:
```python
app.run(debug=True, port=5000)  # Change 5000 to your port
```

#### Change File Size Limit
Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

#### Enable Email
Edit `config.py`:
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

### HTML Version

#### Change File Size Limit
Edit `app.js`:
```javascript
if (file.size > 100 * 1024 * 1024) {  // 100MB
```

#### Change Storage Keys
Edit `app.js`:
```javascript
const STORAGE_KEYS = {
    USERS: 'vault_users',
    FILES: 'vault_files',
    // ...
};
```

---

## 🌐 Deployment Options

### Python Version

#### Option 1: Local Network
```bash
python app.py
# Access from other devices: http://YOUR_IP:5000
```

#### Option 2: Heroku (Free)
```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

#### Option 3: PythonAnywhere (Free)
1. Upload files to PythonAnywhere
2. Configure WSGI
3. Get URL: `https://yourusername.pythonanywhere.com`

#### Option 4: VPS (DigitalOcean, AWS, etc.)
```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### HTML Version

#### Option 1: GitHub Pages (Free)
1. Create GitHub repository
2. Upload all files
3. Settings → Pages → Enable
4. URL: `https://username.github.io/repo-name`

#### Option 2: Netlify (Free)
1. Go to [netlify.com](https://netlify.com)
2. Drag folder to deploy
3. Get instant URL with HTTPS

#### Option 3: Vercel (Free)
```bash
npm i -g vercel
vercel
```

#### Option 4: Local Server
```bash
# Python
python -m http.server 8000

# Node.js
npx http-server

# PHP
php -S localhost:8000
```

---

## 🔒 Security Recommendations

### For Both Versions

1. **Strong Passwords**
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Example: `MyV@ult2024!Secure#`

2. **HTTPS**
   - Always use HTTPS in production
   - Free SSL: Let's Encrypt, Cloudflare

3. **Backups**
   - Regular database backups (Python)
   - Export LocalStorage (HTML)
   - Keep offline copies

4. **Updates**
   - Keep Python/libraries updated
   - Keep browser updated
   - Monitor security advisories

### Python Version Specific

1. **Environment Variables**
   ```bash
   # Use .env file for secrets
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///vault.db
   ```

2. **Production Settings**
   ```python
   app.config['DEBUG'] = False
   app.config['TESTING'] = False
   ```

3. **Firewall**
   - Restrict access to port 5000
   - Use reverse proxy (nginx)

### HTML Version Specific

1. **Content Security Policy**
   ```html
   <meta http-equiv="Content-Security-Policy" 
         content="default-src 'self'">
   ```

2. **Subresource Integrity**
   - Use SRI for external libraries
   - Verify file integrity

---

## 🆘 Troubleshooting

### Python Version

**Problem**: `ModuleNotFoundError`
```bash
# Solution
pip install -r requirements.txt
```

**Problem**: Port already in use
```bash
# Solution: Change port in app.py or kill process
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

**Problem**: Database locked
```bash
# Solution: Close other connections or delete vault.db
rm vault.db
python app.py  # Creates new database
```

### HTML Version

**Problem**: Files not saving
- Enable JavaScript
- Check LocalStorage quota
- Clear browser cache

**Problem**: Can't open file
- Right-click → Open With → Browser
- Or drag into browser window

**Problem**: Slow performance
- Reduce file size
- Use Chrome/Firefox
- Close other tabs

---

## 📚 Documentation

### Python Version
- `README.md` - Arabic documentation
- `README_ENGLISH.md` - English documentation
- `QUICK_START.md` - Quick start guide
- `FEATURES_GUIDE.md` - Feature documentation

### HTML Version
- `README_HTML_VERSION.md` - Complete guide
- `QUICK_START_HTML.md` - Quick start
- This file - Setup guide

---

## 🎓 Learning Resources

### Encryption
- [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)
- [AES Encryption](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2)

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Tutorial](https://flask.palletsprojects.com/tutorial/)

### JavaScript
- [MDN JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)

---

## 📧 Support

For help:
1. Check documentation
2. Review troubleshooting section
3. Check browser/terminal console
4. Open GitHub issue

---

## 🎉 You're Ready!

Choose your version and start encrypting files securely!

**Python Version**: Full-featured, production-ready  
**HTML Version**: Quick, simple, privacy-focused

Both versions provide military-grade encryption for your files! 🔐

---

**Made with ❤️ in Egypt 🇪🇬**

**Version**: 1.0.0  
**Last Updated**: 2024
