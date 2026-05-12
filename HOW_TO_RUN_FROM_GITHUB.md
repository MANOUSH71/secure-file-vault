# 🚀 كيفية تشغيل المشروع من GitHub

## للمستخدمين الجدد - دليل كامل

---

## 📋 المتطلبات الأساسية

قبل ما تبدأ، تأكد إن عندك:

- ✅ **Python 3.8 أو أحدث** - [تحميل Python](https://www.python.org/downloads/)
- ✅ **Git** - [تحميل Git](https://git-scm.com/download/win)
- ✅ **محرر نصوص** (اختياري) - VS Code, Notepad++, إلخ

---

## 🎯 الطريقة 1: التشغيل السريع (للمبتدئين)

### الخطوة 1️⃣: تحميل المشروع

#### الطريقة الأولى - باستخدام Git (موصى بها):

```bash
# افتح Terminal أو Command Prompt
# اذهب للمكان اللي عايز تحمل فيه المشروع
cd Desktop

# استنسخ المشروع
git clone https://github.com/MANOUSH71/secure-file-vault.git

# ادخل لمجلد المشروع
cd secure-file-vault
```

#### الطريقة الثانية - تحميل ZIP:

1. اذهب إلى: https://github.com/MANOUSH71/secure-file-vault
2. اضغط على الزر الأخضر **"Code"**
3. اختر **"Download ZIP"**
4. فك ضغط الملف
5. افتح Terminal في المجلد

---

### الخطوة 2️⃣: تثبيت المكتبات المطلوبة

```bash
# تأكد إنك في مجلد المشروع
cd secure-file-vault

# ثبت المكتبات
pip install -r requirements.txt
```

**ملاحظة:** لو عندك Python 2 و Python 3، استخدم `pip3` بدل `pip`

---

### الخطوة 3️⃣: تشغيل المشروع

```bash
python app.py
```

**ملاحظة:** لو عندك Python 2 و Python 3، استخدم `python3` بدل `python`

---

### الخطوة 4️⃣: فتح المتصفح

افتح المتصفح واذهب إلى:
```
http://localhost:5000
```

أو:
```
http://127.0.0.1:5000
```

---

## 🎊 تم! المشروع شغال!

الآن تقدر:
1. **تسجل حساب جديد**
2. **ترفع وتشفر ملفات**
3. **تنشئ فريق**
4. **تدعو أعضاء**
5. **تستمتع بكل الميزات!**

---

## 🔧 الطريقة 2: التشغيل المتقدم (للمحترفين)

### استخدام Virtual Environment (موصى به):

```bash
# 1. استنسخ المشروع
git clone https://github.com/MANOUSH71/secure-file-vault.git
cd secure-file-vault

# 2. أنشئ بيئة افتراضية
python -m venv venv

# 3. فعّل البيئة الافتراضية
# على Windows:
venv\Scripts\activate

# على Mac/Linux:
# source venv/bin/activate

# 4. ثبت المكتبات
pip install -r requirements.txt

# 5. شغل المشروع
python app.py
```

---

## 📦 المكتبات المطلوبة

المشروع يحتاج هذه المكتبات (موجودة في `requirements.txt`):

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

## 🌐 الوصول من أجهزة أخرى على نفس الشبكة

لو عايز تفتح المشروع من موبايلك أو جهاز تاني على نفس الـ WiFi:

### 1. اعرف الـ IP Address بتاع جهازك:

**على Windows:**
```bash
ipconfig
```
ابحث عن `IPv4 Address` (مثلاً: 192.168.1.100)

**على Mac/Linux:**
```bash
ifconfig
```

### 2. شغل المشروع بـ host=0.0.0.0:

المشروع مضبوط بالفعل على `host='0.0.0.0'` في `app.py`

### 3. افتح من الجهاز التاني:

```
http://192.168.1.100:5000
```
(استبدل 192.168.1.100 بالـ IP بتاعك)

---

## 🆘 حل المشاكل الشائعة

### ❌ **"python is not recognized"**

**المشكلة:** Python مش مثبت أو مش في الـ PATH

**الحل:**
1. حمل Python من: https://www.python.org/downloads/
2. أثناء التثبيت، اختار ✅ **"Add Python to PATH"**
3. أعد تشغيل Terminal

---

### ❌ **"pip is not recognized"**

**الحل:**
```bash
python -m pip install -r requirements.txt
```

---

### ❌ **"Address already in use" أو "Port 5000 is already in use"**

**المشكلة:** البورت 5000 مستخدم من برنامج تاني

**الحل 1 - غير البورت:**
افتح `app.py` وغير السطر الأخير:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # غير 5000 لـ 5001
```

**الحل 2 - اقفل البرنامج اللي مستخدم البورت:**
```bash
# على Windows
netstat -ano | findstr :5000
taskkill /PID <رقم_العملية> /F
```

---

### ❌ **"ModuleNotFoundError: No module named 'flask'"**

**المشكلة:** المكتبات مش مثبتة

**الحل:**
```bash
pip install -r requirements.txt
```

---

### ❌ **"Permission denied" عند التثبيت**

**الحل:**
```bash
pip install --user -r requirements.txt
```

---

### ❌ **المشروع بطيء أو مش شغال**

**الحل:**
1. تأكد إن عندك مساحة كافية على الهارد
2. تأكد إن الـ Antivirus مش بيبلوك المشروع
3. جرب تشغل Terminal كـ Administrator

---

## 🔒 الأمان

### ⚠️ **مهم للاستخدام الحقيقي:**

1. **غير الـ SECRET_KEY:**
   - افتح `app.py`
   - غير السطر: `app.secret_key = secrets.token_hex(32)`
   - أو أنشئ ملف `.env` وحط فيه:
     ```
     SECRET_KEY=your-very-secret-key-here
     ```

2. **اقفل الـ Debug Mode في Production:**
   - في `app.py`، غير:
     ```python
     app.run(debug=False, host='0.0.0.0', port=5000)
     ```

3. **استخدم HTTPS:**
   - للاستخدام الحقيقي، استخدم SSL/TLS

4. **غير إعدادات قاعدة البيانات:**
   - استخدم PostgreSQL أو MySQL بدل SQLite للإنتاج

---

## 📁 هيكل المشروع

بعد التحميل، هتلاقي:

```
secure-file-vault/
├── app.py                  # الملف الرئيسي
├── models.py               # قاعدة البيانات
├── crypto_manager.py       # التشفير
├── config.py               # الإعدادات
├── requirements.txt        # المكتبات
├── templates/              # صفحات HTML
├── static/                 # CSS & JS
├── uploads/                # الملفات المشفرة
└── docs/                   # التوثيق
```

---

## 🎓 للمطورين

### تشغيل في وضع التطوير:

```bash
# 1. استنسخ المشروع
git clone https://github.com/MANOUSH71/secure-file-vault.git
cd secure-file-vault

# 2. أنشئ بيئة افتراضية
python -m venv venv
venv\Scripts\activate

# 3. ثبت المكتبات
pip install -r requirements.txt

# 4. شغل في وضع Debug
python app.py
```

### عمل تعديلات:

```bash
# 1. أنشئ branch جديد
git checkout -b my-feature

# 2. عدل الكود

# 3. احفظ التعديلات
git add .
git commit -m "Add my feature"

# 4. ارفع التعديلات
git push origin my-feature

# 5. افتح Pull Request على GitHub
```

---

## 📚 التوثيق

للمزيد من المعلومات:

- **[FEATURES_GUIDE.md](FEATURES_GUIDE.md)** - شرح كل الميزات
- **[QUICK_START_TEAM.md](QUICK_START_TEAM.md)** - دليل البداية السريع
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - تفاصيل التنفيذ

---

## 🎯 الاستخدام الأساسي

### 1. إنشاء حساب:
```
http://localhost:5000
→ Register
→ املأ البيانات
→ Create Account
```

### 2. تشفير ملف:
```
Dashboard
→ اسحب ملف للمربع الأزرق
→ اختر طريقة التشفير
→ اكتب كلمة سر
→ Encrypt File
```

### 3. إنشاء فريق:
```
Teams
→ Create Team
→ اكتب اسم الفريق
→ Create
```

### 4. دعوة أعضاء:
```
Teams
→ View (على الفريق)
→ Invite Member
→ Generate Invite
→ انسخ اللينك وشاركه
```

---

## 🌟 الميزات الرئيسية

- 🔒 **4 طرق تشفير** (AES, ChaCha20, Fernet, RSA)
- 👥 **إدارة الفرق** (حتى 8 أعضاء)
- 📊 **لوحة تحليلات** مع رسوم بيانية
- 🔔 **نظام إشعارات** متكامل
- 🛡️ **مصادقة ثنائية** (2FA)
- 📋 **سجل تدقيق** كامل
- 📤 **طلبات ملفات** عامة
- ⚙️ **إدارة الجلسات**

---

## 💡 نصائح

1. **استخدم Chrome أو Firefox** للحصول على أفضل تجربة
2. **فعّل 2FA** لحماية حسابك
3. **استخدم كلمات سر قوية** للتشفير
4. **راجع سجل التدقيق** بانتظام
5. **احتفظ بنسخة احتياطية** من قاعدة البيانات

---

## 📞 الدعم

لو واجهت أي مشكلة:

1. **تحقق من التوثيق** في مجلد `docs/`
2. **افتح Issue على GitHub:** https://github.com/MANOUSH71/secure-file-vault/issues
3. **تحقق من الـ Issues الموجودة** - ممكن حد حل المشكلة قبل كده

---

## 🎉 خلاص!

المشروع دلوقتي شغال على جهازك!

**استمتع بالتشفير الآمن! 🔐**

---

## 📝 ملاحظات إضافية

### للاستخدام على Server:

لو عايز تشغل المشروع على سيرفر حقيقي:

1. **استخدم Gunicorn:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **استخدم Nginx كـ Reverse Proxy**

3. **استخدم SSL Certificate** (Let's Encrypt)

4. **استخدم قاعدة بيانات أقوى** (PostgreSQL)

---

**آخر تحديث:** مايو 2026  
**الإصدار:** 2.0.0 - Team Edition
