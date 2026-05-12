# 🛡️ Asset & Risk Management System

## Professional Full-Stack Enterprise Application

A complete enterprise-level Asset & Risk Management System built with FastAPI, PostgreSQL, Supabase, and React/Next.js.

## 🎉 **Backend Status: 100% COMPLETE** ✅

The backend API is fully functional with 40+ endpoints, complete authentication, and comprehensive documentation!

---

## 🚀 Features

### ✅ Authentication & Security
- User registration and login
- JWT authentication
- Role-Based Access Control (Admin, Manager, Employee)
- Email verification and password reset
- Secure API endpoints
- Audit logging for all important actions

### 📊 Dashboard
- Modern analytics dashboard
- Total assets, vulnerabilities, active users
- Risk distribution charts
- Critical assets overview
- Recent activities timeline
- Pie charts, bar charts, statistics cards

### 🏢 Asset Management
- Create, update, delete, and view assets
- Asset categories
- Asset criticality levels (Low, Medium, High, Critical)
- Asset owner assignment
- Department relation
- Search and filtering system

### ⚠️ Vulnerability & Risk Management
- Assign vulnerabilities to assets
- Risk scoring system
- Severity levels
- Risk status tracking
- Mitigation notes
- Vulnerability history

### 🔔 Notifications System
- Real-time notifications
- Notification bell UI
- Alerts for high-risk assets
- Alerts for new vulnerabilities
- Alerts for user activities

### 📁 File Storage (Supabase)
- Upload images
- Upload PDF reports
- Store attachments securely

### 🎨 Modern UI/UX
- Responsive design
- Enterprise-style interface
- Clean and professional
- Dark Mode support
- Sidebar navigation
- Modern cards and tables
- Smooth animations
- Loading skeletons

### 📄 Additional Features
- Export reports as PDF
- Real-time updates using Supabase Realtime
- Pagination
- Advanced filtering
- Global search
- User activity tracking
- API Documentation (Swagger/OpenAPI)

---

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **Supabase** - Backend as a Service
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **JWT** - Authentication
- **Pydantic** - Data validation

### Frontend
- **React/Next.js** - UI framework
- **Tailwind CSS** - Styling
- **Shadcn/UI** - Component library
- **React Query** - Data fetching
- **Zustand** - State management
- **Recharts** - Data visualization
- **React Hook Form** - Form handling

---

## 📁 Project Structure

```
asset-risk-management/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py
│   │   │       │   ├── users.py
│   │   │       │   ├── assets.py
│   │   │       │   ├── vulnerabilities.py
│   │   │       │   ├── risks.py
│   │   │       │   ├── notifications.py
│   │   │       │   ├── dashboard.py
│   │   │       │   └── reports.py
│   │   │       └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── organization.py
│   │   │   ├── department.py
│   │   │   ├── asset.py
│   │   │   ├── vulnerability.py
│   │   │   ├── risk.py
│   │   │   ├── notification.py
│   │   │   ├── audit_log.py
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── asset.py
│   │   │   ├── vulnerability.py
│   │   │   ├── risk.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── asset_service.py
│   │   │   ├── risk_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── supabase_service.py
│   │   │   └── __init__.py
│   │   └── utils/
│   │       ├── email.py
│   │       ├── pdf_generator.py
│   │       └── __init__.py
│   ├── alembic/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── layout/
    │   │   │   ├── Sidebar.tsx
    │   │   │   ├── Header.tsx
    │   │   │   └── Layout.tsx
    │   │   ├── dashboard/
    │   │   │   ├── StatsCard.tsx
    │   │   │   ├── RiskChart.tsx
    │   │   │   └── ActivityTimeline.tsx
    │   │   ├── assets/
    │   │   │   ├── AssetTable.tsx
    │   │   │   ├── AssetForm.tsx
    │   │   │   └── AssetCard.tsx
    │   │   ├── vulnerabilities/
    │   │   ├── notifications/
    │   │   └── common/
    │   ├── pages/
    │   │   ├── Dashboard.tsx
    │   │   ├── Assets.tsx
    │   │   ├── Vulnerabilities.tsx
    │   │   ├── Risks.tsx
    │   │   ├── Users.tsx
    │   │   └── Settings.tsx
    │   ├── services/
    │   │   └── api.ts
    │   ├── hooks/
    │   ├── store/
    │   ├── types/
    │   └── utils/
    ├── package.json
    └── tailwind.config.js
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Supabase account

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/api/docs

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Edit .env.local with your configuration

# Start development server
npm run dev
```

The frontend will be available at: http://localhost:3000

---

## 📊 Database Schema

### Core Tables

#### Users
- id, email, username, password_hash
- first_name, last_name, role
- organization_id, department_id
- is_active, is_verified
- created_at, updated_at

#### Organizations
- id, name, description
- created_at, updated_at

#### Departments
- id, name, organization_id
- created_at, updated_at

#### Assets
- id, name, description, category
- criticality_level, status
- owner_id, department_id
- location, purchase_date, value
- created_at, updated_at

#### Vulnerabilities
- id, title, description
- severity, cvss_score
- asset_id, discovered_date
- status, mitigation_notes
- created_at, updated_at

#### Risks
- id, title, description
- risk_score, likelihood, impact
- asset_id, vulnerability_id
- status, mitigation_plan
- created_at, updated_at

#### Notifications
- id, user_id, title, message
- type, is_read, priority
- created_at

#### Audit_Logs
- id, user_id, action, entity_type
- entity_id, details
- ip_address, user_agent
- created_at

---

## 🔐 API Endpoints

### Authentication
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
GET    /api/v1/auth/verify-email/{token}
```

### Users
```
GET    /api/v1/users
GET    /api/v1/users/{id}
POST   /api/v1/users
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}
GET    /api/v1/users/me
PUT    /api/v1/users/me
```

### Assets
```
GET    /api/v1/assets
GET    /api/v1/assets/{id}
POST   /api/v1/assets
PUT    /api/v1/assets/{id}
DELETE /api/v1/assets/{id}
GET    /api/v1/assets/search
GET    /api/v1/assets/categories
```

### Vulnerabilities
```
GET    /api/v1/vulnerabilities
GET    /api/v1/vulnerabilities/{id}
POST   /api/v1/vulnerabilities
PUT    /api/v1/vulnerabilities/{id}
DELETE /api/v1/vulnerabilities/{id}
GET    /api/v1/vulnerabilities/asset/{asset_id}
```

### Risks
```
GET    /api/v1/risks
GET    /api/v1/risks/{id}
POST   /api/v1/risks
PUT    /api/v1/risks/{id}
DELETE /api/v1/risks/{id}
GET    /api/v1/risks/calculate
```

### Dashboard
```
GET    /api/v1/dashboard/stats
GET    /api/v1/dashboard/risk-distribution
GET    /api/v1/dashboard/recent-activities
GET    /api/v1/dashboard/critical-assets
```

### Notifications
```
GET    /api/v1/notifications
GET    /api/v1/notifications/unread
PUT    /api/v1/notifications/{id}/read
PUT    /api/v1/notifications/mark-all-read
DELETE /api/v1/notifications/{id}
```

### Reports
```
GET    /api/v1/reports/assets/export
GET    /api/v1/reports/vulnerabilities/export
GET    /api/v1/reports/risks/pdf
GET    /api/v1/reports/audit-log
```

---

## 🎨 UI Components

### Dashboard
- Statistics cards (Total Assets, Vulnerabilities, Users)
- Risk distribution pie chart
- Asset criticality bar chart
- Recent activities timeline
- Critical assets table
- Quick actions panel

### Asset Management
- Asset list with filters
- Asset detail view
- Create/Edit asset form
- Asset criticality badge
- Asset status indicator
- Department assignment

### Vulnerability Management
- Vulnerability list
- Severity badges
- CVSS score display
- Mitigation tracking
- Vulnerability timeline
- Asset relationship view

### Risk Management
- Risk matrix
- Risk scoring calculator
- Mitigation plan editor
- Risk status workflow
- Impact/Likelihood grid

### Notifications
- Notification bell with count
- Notification dropdown
- Real-time updates
- Priority indicators
- Mark as read functionality

---

## 🔒 Security Features

### Authentication
- JWT tokens with refresh mechanism
- Password hashing with bcrypt
- Email verification
- Password reset flow
- Session management

### Authorization
- Role-based access control (RBAC)
- Permission-based endpoints
- Resource ownership validation
- Admin-only operations

### Data Protection
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection
- CSRF protection
- Rate limiting
- Input validation (Pydantic)

### Audit Trail
- All important actions logged
- User activity tracking
- IP address logging
- Timestamp tracking
- Change history

---

## 📈 Performance Optimization

- Database indexing
- Query optimization
- Pagination for large datasets
- Caching strategies
- Lazy loading
- Connection pooling
- Async operations

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

---

## 📦 Deployment

### Backend (Docker)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Vercel/Netlify)
```bash
npm run build
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👥 Team

- **Backend Lead**: FastAPI & PostgreSQL
- **Frontend Lead**: React & Tailwind CSS
- **DevOps**: Docker & CI/CD
- **Security**: Authentication & Authorization

---

## 📞 Support

For support, email support@assetrisk.com or join our Slack channel.

---

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Core authentication
- ✅ Asset management
- ✅ Vulnerability tracking
- ✅ Basic dashboard

### Phase 2
- 🔄 Advanced risk scoring
- 🔄 Compliance tracking
- 🔄 Integration with security tools
- 🔄 Mobile app

### Phase 3
- 📅 AI-powered risk prediction
- 📅 Automated vulnerability scanning
- 📅 Advanced analytics
- 📅 Multi-tenant support

---

**Built with ❤️ for Enterprise Cybersecurity**
