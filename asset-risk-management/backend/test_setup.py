"""
Test Backend Setup
Quick script to verify all imports and configurations
"""

import sys

print("=" * 60)
print("Testing Asset & Risk Management System Backend Setup")
print("=" * 60)

# Test 1: Core imports
print("\n1. Testing core imports...")
try:
    import fastapi
    import uvicorn
    import sqlalchemy
    import pydantic
    print("   ✓ Core packages imported successfully")
except ImportError as e:
    print(f"   ✗ Error importing core packages: {e}")
    sys.exit(1)

# Test 2: Security imports
print("\n2. Testing security imports...")
try:
    from jose import jwt
    from passlib.context import CryptContext
    print("   ✓ Security packages imported successfully")
except ImportError as e:
    print(f"   ✗ Error importing security packages: {e}")
    sys.exit(1)

# Test 3: Application imports
print("\n3. Testing application imports...")
try:
    from app.core.config import settings
    from app.core.database import Base, engine
    from app.core.security import get_password_hash, verify_password
    print("   ✓ Application core imported successfully")
except ImportError as e:
    print(f"   ✗ Error importing application core: {e}")
    sys.exit(1)

# Test 4: Models
print("\n4. Testing models...")
try:
    from app.models import (
        User, Organization, Department, Asset,
        Vulnerability, Risk, Notification, AuditLog
    )
    print("   ✓ All models imported successfully")
except ImportError as e:
    print(f"   ✗ Error importing models: {e}")
    sys.exit(1)

# Test 5: Schemas
print("\n5. Testing schemas...")
try:
    from app.schemas import (
        UserCreate, AssetCreate, VulnerabilityCreate, RiskCreate
    )
    print("   ✓ All schemas imported successfully")
except ImportError as e:
    print(f"   ✗ Error importing schemas: {e}")
    sys.exit(1)

# Test 6: API endpoints
print("\n6. Testing API endpoints...")
try:
    from app.api.v1.endpoints import (
        auth, users, assets, vulnerabilities, risks, dashboard, notifications
    )
    print("   ✓ All API endpoints imported successfully")
except ImportError as e:
    print(f"   ✗ Error importing API endpoints: {e}")
    sys.exit(1)

# Test 7: Configuration
print("\n7. Testing configuration...")
try:
    print(f"   App Name: {settings.APP_NAME}")
    print(f"   App Version: {settings.APP_VERSION}")
    print(f"   Database URL: {settings.DATABASE_URL[:30]}...")
    print("   ✓ Configuration loaded successfully")
except Exception as e:
    print(f"   ✗ Error loading configuration: {e}")
    sys.exit(1)

# Test 8: Password hashing
print("\n8. Testing password hashing...")
try:
    test_password = "TestPassword123!"
    hashed = get_password_hash(test_password)
    verified = verify_password(test_password, hashed)
    if verified:
        print("   ✓ Password hashing working correctly")
    else:
        print("   ✗ Password verification failed")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Error testing password hashing: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All tests passed! Backend is ready to run.")
print("=" * 60)
print("\nNext steps:")
print("1. Set up PostgreSQL database")
print("2. Copy .env.example to .env and configure")
print("3. Run: alembic upgrade head")
print("4. Run: uvicorn main:app --reload")
print("\nAPI will be available at: http://localhost:8000")
print("API Docs: http://localhost:8000/api/docs")
print("=" * 60)
