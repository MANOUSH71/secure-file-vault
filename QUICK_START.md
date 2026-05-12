# ⚡ Quick Start Guide - Secure File Vault Pro

## 🚀 Get Started in 5 Minutes

### Step 1: Download & Extract (1 minute)
1. Download the project ZIP file
2. Extract to any folder on your computer
3. Remember the folder location

### Step 2: Install Python (2 minutes - skip if already installed)
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.8+
3. **Important**: Check "Add Python to PATH" during installation
4. Install

### Step 3: Install Dependencies (1 minute)
1. Open the project folder
2. Hold `Shift` + Right-click → "Open PowerShell here"
3. Run:
```bash
pip install -r requirements.txt
```

### Step 4: Run Application (30 seconds)
```bash
python app.py
```

### Step 5: Open Browser (30 seconds)
Go to: `http://localhost:5000`

## ✅ That's It!

You're ready to encrypt files securely!

---

## 🎯 First Time Usage

### Create Account
1. Click "Create Account"
2. Enter username, email, password
3. Click "Register"

### Encrypt Your First File
1. Drag & drop a file
2. Choose "AES-256-GCM" (recommended)
3. Enter a strong password
4. Click "Encrypt File"

### Decrypt File
1. Click "Decrypt" next to your file
2. Enter the password you used
3. File downloads automatically

---

## 🆘 Quick Troubleshooting

**Can't install Python packages?**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Port 5000 already in use?**
Edit `app.py` and change port to 5001:
```python
app.run(debug=True, port=5001)
```

**Application won't start?**
Make sure you're in the correct folder:
```bash
cd "path\to\project\folder"
python app.py
```

---

## 📚 Need More Help?

Read the full documentation: `README_ENGLISH.md`

---

**Happy Encrypting! 🔐**
