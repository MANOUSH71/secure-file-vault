# Backend Setup Guide

## Quick Start (Development)

### 1. Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env with your configuration
# At minimum, update:
# - DATABASE_URL (PostgreSQL connection string)
# - SECRET_KEY (generate a secure random key)
```

### 3. Set Up Database

#### Option A: Using PostgreSQL (Recommended for Production)

```bash
# Install PostgreSQL if not already installed
# Windows: Download from https://www.postgresql.org/download/windows/
# Linux: sudo apt-get install postgresql postgresql-contrib
# Mac: brew install postgresql

# Create database
psql -U postgres
CREATE DATABASE asset_risk_db;
CREATE USER asset_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE asset_risk_db TO asset_user;
\q

# Update DATABASE_URL in .env:
DATABASE_URL=postgresql://asset_user:your_password@localhost:5432/asset_risk_db
```

#### Option B: Using SQLite (Quick Testing Only)

```bash
# Update DATABASE_URL in .env:
DATABASE_URL=sqlite:///./asset_risk.db
```

### 4. Run Database Migrations

```bash
# Initialize Alembic (only needed once)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Test Setup

```bash
# Run the test script to verify everything is working
python test_setup.py
```

### 6. Start the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7. Access the API

- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/api/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

---

## Testing the API

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "password": "SecurePassword123!",
    "first_name": "Admin",
    "last_name": "User",
    "role": "admin"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "SecurePassword123!"
  }'
```

Save the `access_token` from the response.

### 3. Create an Asset

```bash
curl -X POST "http://localhost:8000/api/v1/assets" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Production Server",
    "description": "Main production web server",
    "category": "server",
    "criticality_level": "critical",
    "status": "active",
    "location": "Data Center A",
    "ip_address": "192.168.1.100"
  }'
```

### 4. Get Dashboard Stats

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/stats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Using Swagger UI

1. Open http://localhost:8000/api/docs
2. Click "Authorize" button
3. Login using the `/api/v1/auth/token` endpoint
4. Enter your credentials
5. Click "Authorize"
6. Now you can test all endpoints interactively!

---

## Database Management

### Create a New Migration

```bash
# After modifying models
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>
```

### Rollback Migrations

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

### View Migration History

```bash
# Show current revision
alembic current

# Show migration history
alembic history
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError"

```bash
# Make sure all dependencies are installed
pip install -r requirements.txt
```

### Issue: "Database connection failed"

```bash
# Check if PostgreSQL is running
# Windows: Check Services
# Linux: sudo systemctl status postgresql
# Mac: brew services list

# Verify DATABASE_URL in .env is correct
```

### Issue: "Alembic command not found"

```bash
# Make sure virtual environment is activated
# Install alembic explicitly
pip install alembic
```

### Issue: "JWT decode error"

```bash
# Make sure SECRET_KEY in .env is at least 32 characters
# Generate a new one:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Production Deployment

### 1. Environment Variables

```bash
# Set production values
DEBUG=False
SECRET_KEY=<generate-strong-random-key>
DATABASE_URL=<production-database-url>
CORS_ORIGINS=https://yourdomain.com
```

### 2. Use Production Server

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 3. Docker Deployment

```bash
# Build image
docker build -t asset-risk-backend .

# Run container
docker run -d -p 8000:8000 --env-file .env asset-risk-backend
```

---

## API Endpoints Summary

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/token` - OAuth2 token (for Swagger)

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users` - List all users (Admin)
- `GET /api/v1/users/{id}` - Get user by ID (Admin)
- `PUT /api/v1/users/{id}` - Update user (Admin)
- `DELETE /api/v1/users/{id}` - Delete user (Admin)

### Assets
- `GET /api/v1/assets` - List assets (with filters)
- `GET /api/v1/assets/{id}` - Get asset by ID
- `POST /api/v1/assets` - Create asset
- `PUT /api/v1/assets/{id}` - Update asset
- `DELETE /api/v1/assets/{id}` - Delete asset
- `GET /api/v1/assets/categories` - Get asset categories
- `GET /api/v1/assets/search` - Search assets

### Vulnerabilities
- `GET /api/v1/vulnerabilities` - List vulnerabilities
- `GET /api/v1/vulnerabilities/{id}` - Get vulnerability
- `POST /api/v1/vulnerabilities` - Create vulnerability
- `PUT /api/v1/vulnerabilities/{id}` - Update vulnerability
- `DELETE /api/v1/vulnerabilities/{id}` - Delete vulnerability
- `GET /api/v1/vulnerabilities/asset/{asset_id}` - Get by asset

### Risks
- `GET /api/v1/risks` - List risks
- `GET /api/v1/risks/{id}` - Get risk
- `POST /api/v1/risks` - Create risk
- `PUT /api/v1/risks/{id}` - Update risk
- `DELETE /api/v1/risks/{id}` - Delete risk
- `GET /api/v1/risks/calculate` - Calculate risk score

### Dashboard
- `GET /api/v1/dashboard/stats` - Get statistics
- `GET /api/v1/dashboard/risk-distribution` - Risk distribution
- `GET /api/v1/dashboard/asset-criticality` - Asset criticality
- `GET /api/v1/dashboard/vulnerability-severity` - Vulnerability severity
- `GET /api/v1/dashboard/recent-activities` - Recent activities
- `GET /api/v1/dashboard/critical-assets` - Critical assets

### Notifications
- `GET /api/v1/notifications` - List notifications
- `GET /api/v1/notifications/unread` - Get unread notifications
- `PUT /api/v1/notifications/{id}/read` - Mark as read
- `PUT /api/v1/notifications/mark-all-read` - Mark all as read
- `DELETE /api/v1/notifications/{id}` - Delete notification

---

## Next Steps

1. ✅ Backend API is ready
2. 🔄 Set up frontend (React/Next.js)
3. 🔄 Configure Supabase for file storage
4. 🔄 Add real-time notifications
5. 🔄 Implement PDF report generation
6. 🔄 Add comprehensive tests
7. 🔄 Deploy to production

---

**Happy Coding! 🚀**
