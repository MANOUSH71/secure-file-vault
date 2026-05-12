# ⚡ Quick Start Guide

## Get the Asset & Risk Management System Running in 10 Minutes

---

## 🎯 What You'll Build

A complete enterprise-level Asset & Risk Management System with:
- ✅ User authentication & authorization
- ✅ Asset management dashboard
- ✅ Vulnerability tracking
- ✅ Risk assessment
- ✅ Real-time notifications
- ✅ File storage
- ✅ PDF reports
- ✅ Modern UI with dark mode

---

## 📋 Prerequisites

```bash
# Check versions
python --version  # Should be 3.10+
node --version    # Should be 18+
psql --version    # Should be 14+
```

---

## 🚀 Installation (5 Minutes)

### 1. Clone & Setup

```bash
# Navigate to project
cd asset-risk-management

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb asset_risk_db

# Or using psql
psql -U postgres
CREATE DATABASE asset_risk_db;
\q
```

### 3. Environment Configuration

**Backend (.env)**:
```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/asset_risk_db
SECRET_KEY=your-secret-key-min-32-characters-long
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

**Frontend (.env.local)**:
```bash
cd frontend
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 4. Run Migrations

```bash
cd backend
alembic upgrade head
```

---

## 🎮 Running the Application (2 Minutes)

### Terminal 1: Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload
```

✅ Backend running at: http://localhost:8000
📚 API Docs: http://localhost:8000/api/docs

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

✅ Frontend running at: http://localhost:3000

---

## 🎨 First Steps

### 1. Register an Account

Navigate to: http://localhost:3000/register

```
Email: admin@example.com
Password: Admin@123456
First Name: Admin
Last Name: User
Role: Admin
```

### 2. Login

Navigate to: http://localhost:3000/login

Use the credentials you just created.

### 3. Explore Dashboard

You'll see:
- 📊 Statistics cards
- 📈 Risk distribution chart
- 📋 Recent activities
- 🔔 Notifications

### 4. Create Your First Asset

1. Click "Assets" in sidebar
2. Click "Add Asset" button
3. Fill in the form:
   ```
   Name: Production Server
   Category: Server
   Criticality: High
   Status: Active
   Description: Main production server
   ```
4. Click "Create Asset"

### 5. Add a Vulnerability

1. Click "Vulnerabilities" in sidebar
2. Click "Add Vulnerability"
3. Fill in:
   ```
   Title: Outdated SSL Certificate
   Severity: High
   CVSS Score: 7.5
   Asset: Production Server
   Status: Open
   ```
4. Click "Create"

### 6. Assess Risk

1. Click "Risks" in sidebar
2. Click "Add Risk"
3. Fill in:
   ```
   Title: SSL Certificate Expiration Risk
   Asset: Production Server
   Vulnerability: Outdated SSL Certificate
   Likelihood: High
   Impact: High
   Status: Open
   ```
4. System calculates risk score automatically

---

## 📊 Sample Data (Optional)

Load sample data for testing:

```bash
cd backend
python scripts/seed_data.py
```

This creates:
- 5 sample users
- 20 sample assets
- 15 vulnerabilities
- 10 risks
- Sample notifications

---

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test@123456",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test@123456"
  }'
```

### Test Frontend

Open browser and navigate through:
1. ✅ Registration page
2. ✅ Login page
3. ✅ Dashboard
4. ✅ Assets page
5. ✅ Vulnerabilities page
6. ✅ Risks page

---

## 🎯 Key Features to Try

### 1. Dashboard Analytics
- View total assets count
- See vulnerability distribution
- Check risk levels
- Monitor recent activities

### 2. Asset Management
- Create new assets
- Edit asset details
- Assign criticality levels
- Filter and search assets
- Export asset list

### 3. Vulnerability Tracking
- Add vulnerabilities
- Assign to assets
- Set severity levels
- Track mitigation status
- View vulnerability history

### 4. Risk Assessment
- Create risk assessments
- Calculate risk scores
- Link to assets and vulnerabilities
- Track mitigation plans
- Generate risk reports

### 5. Notifications
- Real-time alerts
- High-risk asset notifications
- New vulnerability alerts
- Mark as read/unread
- Notification history

### 6. File Management
- Upload asset images
- Attach PDF reports
- Store documentation
- Download attachments

### 7. User Management (Admin)
- Create users
- Assign roles
- Manage permissions
- View user activity
- Deactivate users

### 8. Reports
- Export assets to Excel
- Generate PDF reports
- Vulnerability summaries
- Risk assessment reports
- Audit logs

---

## 🔧 Troubleshooting

### Backend Issues

**Database Connection Error**:
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check connection
psql -U postgres -d asset_risk_db
```

**Module Not Found**:
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Port Already in Use**:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Dependencies Error**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Port Already in Use**:
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

**API Connection Error**:
- Check backend is running
- Verify API URL in `.env.local`
- Check CORS settings

---

## 📚 Next Steps

### 1. Customize
- Update branding
- Modify color scheme
- Add custom fields
- Configure email templates

### 2. Integrate
- Connect to Supabase
- Set up file storage
- Enable real-time updates
- Configure email service

### 3. Deploy
- Set up production database
- Deploy backend to cloud
- Deploy frontend to Vercel
- Configure domain

### 4. Secure
- Enable HTTPS
- Set up firewall
- Configure rate limiting
- Enable audit logging

### 5. Monitor
- Set up error tracking
- Configure logging
- Add performance monitoring
- Set up alerts

---

## 🎓 Learning Resources

### Backend
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/en/latest/)

### Frontend
- [Next.js Learn](https://nextjs.org/learn)
- [React Query](https://tanstack.com/query/latest)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Database
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [Database Design](https://www.lucidchart.com/pages/database-diagram/database-design)

---

## 💡 Pro Tips

1. **Use API Docs**: Visit http://localhost:8000/api/docs to test all endpoints
2. **Check Logs**: Monitor terminal output for errors
3. **Use Dark Mode**: Toggle in settings for better UX
4. **Keyboard Shortcuts**: Learn shortcuts for faster navigation
5. **Export Data**: Regularly export data for backup

---

## 🆘 Getting Help

### Documentation
- README.md - Project overview
- IMPLEMENTATION_GUIDE.md - Detailed implementation
- API_DOCUMENTATION.md - API reference

### Community
- GitHub Issues
- Discord Server
- Stack Overflow

### Support
- Email: support@assetrisk.com
- Documentation: https://docs.assetrisk.com

---

## ✅ Checklist

Before going to production:

- [ ] Change default SECRET_KEY
- [ ] Update database credentials
- [ ] Configure Supabase
- [ ] Set up email service
- [ ] Enable HTTPS
- [ ] Configure backups
- [ ] Set up monitoring
- [ ] Test all features
- [ ] Review security settings
- [ ] Update documentation

---

## 🎉 Success!

You now have a fully functional Asset & Risk Management System!

**What's Next?**
1. Explore all features
2. Customize to your needs
3. Add your data
4. Invite team members
5. Deploy to production

---

**Happy Managing! 🛡️**
