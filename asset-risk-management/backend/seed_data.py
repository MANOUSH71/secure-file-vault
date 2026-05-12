"""
Seed Database with Sample Data
Run this script to populate the database with sample data for testing
"""

from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import random

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models import (
    User, Organization, Department, Asset, Vulnerability, Risk, Notification, AuditLog
)
from app.models.user import UserRole
from app.models.asset import AssetCategory, CriticalityLevel, AssetStatus
from app.models.vulnerability import VulnerabilitySeverity, VulnerabilityStatus
from app.models.risk import RiskLevel, RiskStatus
from app.models.notification import NotificationType, NotificationPriority

def create_sample_data():
    """Create sample data for testing"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Creating sample data...")
        
        # 1. Create Organization
        print("\n1. Creating organization...")
        org = Organization(
            name="TechCorp Inc.",
            description="Leading technology company"
        )
        db.add(org)
        db.commit()
        db.refresh(org)
        print(f"   ✓ Created organization: {org.name}")
        
        # 2. Create Departments
        print("\n2. Creating departments...")
        departments = [
            Department(name="IT Security", organization_id=org.id, description="Information Security Team"),
            Department(name="Development", organization_id=org.id, description="Software Development Team"),
            Department(name="Operations", organization_id=org.id, description="IT Operations Team"),
            Department(name="Infrastructure", organization_id=org.id, description="Infrastructure Team"),
        ]
        db.add_all(departments)
        db.commit()
        print(f"   ✓ Created {len(departments)} departments")
        
        # 3. Create Users
        print("\n3. Creating users...")
        users = [
            User(
                email="admin@techcorp.com",
                username="admin",
                password_hash=get_password_hash("Admin123!"),
                first_name="Admin",
                last_name="User",
                role=UserRole.ADMIN,
                organization_id=org.id,
                department_id=departments[0].id,
                is_active=True,
                is_verified=True
            ),
            User(
                email="manager@techcorp.com",
                username="manager",
                password_hash=get_password_hash("Manager123!"),
                first_name="Security",
                last_name="Manager",
                role=UserRole.MANAGER,
                organization_id=org.id,
                department_id=departments[0].id,
                is_active=True,
                is_verified=True
            ),
            User(
                email="john.doe@techcorp.com",
                username="johndoe",
                password_hash=get_password_hash("Employee123!"),
                first_name="John",
                last_name="Doe",
                role=UserRole.EMPLOYEE,
                organization_id=org.id,
                department_id=departments[1].id,
                is_active=True,
                is_verified=True
            ),
            User(
                email="jane.smith@techcorp.com",
                username="janesmith",
                password_hash=get_password_hash("Employee123!"),
                first_name="Jane",
                last_name="Smith",
                role=UserRole.EMPLOYEE,
                organization_id=org.id,
                department_id=departments[2].id,
                is_active=True,
                is_verified=True
            ),
        ]
        db.add_all(users)
        db.commit()
        print(f"   ✓ Created {len(users)} users")
        print("   Default credentials:")
        print("   - admin@techcorp.com / Admin123!")
        print("   - manager@techcorp.com / Manager123!")
        print("   - john.doe@techcorp.com / Employee123!")
        
        # 4. Create Assets
        print("\n4. Creating assets...")
        assets = [
            Asset(
                name="Production Web Server",
                description="Main production web server hosting customer-facing applications",
                category=AssetCategory.SERVER,
                criticality_level=CriticalityLevel.CRITICAL,
                status=AssetStatus.ACTIVE,
                owner_id=users[2].id,
                department_id=departments[2].id,
                location="Data Center A - Rack 12",
                ip_address="192.168.1.100",
                mac_address="00:1B:44:11:3A:B7",
                serial_number="SRV-2024-001",
                purchase_date=date(2023, 1, 15),
                value=15000.00
            ),
            Asset(
                name="Database Server",
                description="PostgreSQL database server for production data",
                category=AssetCategory.DATABASE,
                criticality_level=CriticalityLevel.CRITICAL,
                status=AssetStatus.ACTIVE,
                owner_id=users[2].id,
                department_id=departments[3].id,
                location="Data Center A - Rack 13",
                ip_address="192.168.1.101",
                mac_address="00:1B:44:11:3A:B8",
                serial_number="DB-2024-001",
                purchase_date=date(2023, 2, 20),
                value=20000.00
            ),
            Asset(
                name="Employee Workstation - Dev01",
                description="Development workstation for software engineers",
                category=AssetCategory.WORKSTATION,
                criticality_level=CriticalityLevel.MEDIUM,
                status=AssetStatus.ACTIVE,
                owner_id=users[2].id,
                department_id=departments[1].id,
                location="Office Floor 3",
                ip_address="192.168.2.50",
                mac_address="00:1B:44:11:3A:C1",
                serial_number="WS-2024-050",
                purchase_date=date(2024, 1, 10),
                value=2500.00
            ),
            Asset(
                name="Core Network Router",
                description="Main network router for internal traffic",
                category=AssetCategory.NETWORK_DEVICE,
                criticality_level=CriticalityLevel.HIGH,
                status=AssetStatus.ACTIVE,
                owner_id=users[3].id,
                department_id=departments[3].id,
                location="Data Center A - Network Room",
                ip_address="192.168.0.1",
                mac_address="00:1B:44:11:3A:D1",
                serial_number="RTR-2024-001",
                purchase_date=date(2022, 6, 1),
                value=8000.00
            ),
            Asset(
                name="Customer Portal Application",
                description="Web application for customer self-service",
                category=AssetCategory.APPLICATION,
                criticality_level=CriticalityLevel.HIGH,
                status=AssetStatus.ACTIVE,
                owner_id=users[2].id,
                department_id=departments[1].id,
                location="Cloud - AWS US-East-1",
                purchase_date=date(2023, 3, 1),
                value=50000.00
            ),
            Asset(
                name="Backup Server",
                description="Backup and disaster recovery server",
                category=AssetCategory.SERVER,
                criticality_level=CriticalityLevel.HIGH,
                status=AssetStatus.ACTIVE,
                owner_id=users[3].id,
                department_id=departments[2].id,
                location="Data Center B - Rack 5",
                ip_address="192.168.1.200",
                mac_address="00:1B:44:11:3A:E1",
                serial_number="BKP-2024-001",
                purchase_date=date(2023, 4, 15),
                value=12000.00
            ),
        ]
        db.add_all(assets)
        db.commit()
        print(f"   ✓ Created {len(assets)} assets")
        
        # 5. Create Vulnerabilities
        print("\n5. Creating vulnerabilities...")
        vulnerabilities = [
            Vulnerability(
                title="Outdated SSL/TLS Certificate",
                description="SSL certificate is expiring in 30 days and needs renewal",
                severity=VulnerabilitySeverity.MEDIUM,
                cvss_score=5.3,
                cve_id="CVE-2024-0001",
                asset_id=assets[0].id,
                discovered_date=date.today() - timedelta(days=5),
                status=VulnerabilityStatus.OPEN,
                mitigation_notes="Schedule certificate renewal with IT team"
            ),
            Vulnerability(
                title="SQL Injection Vulnerability",
                description="Potential SQL injection in user input validation",
                severity=VulnerabilitySeverity.CRITICAL,
                cvss_score=9.8,
                cve_id="CVE-2024-0002",
                asset_id=assets[4].id,
                discovered_date=date.today() - timedelta(days=2),
                status=VulnerabilityStatus.IN_PROGRESS,
                mitigation_notes="Implementing parameterized queries and input validation"
            ),
            Vulnerability(
                title="Unpatched Operating System",
                description="Critical security patches not applied to OS",
                severity=VulnerabilitySeverity.HIGH,
                cvss_score=7.5,
                cve_id="CVE-2024-0003",
                asset_id=assets[1].id,
                discovered_date=date.today() - timedelta(days=10),
                status=VulnerabilityStatus.OPEN,
                mitigation_notes="Schedule maintenance window for patching"
            ),
            Vulnerability(
                title="Weak Password Policy",
                description="Password complexity requirements not enforced",
                severity=VulnerabilitySeverity.MEDIUM,
                cvss_score=5.0,
                asset_id=assets[4].id,
                discovered_date=date.today() - timedelta(days=15),
                status=VulnerabilityStatus.RESOLVED,
                mitigation_notes="Updated password policy to require 12+ characters with complexity",
                resolution_date=date.today() - timedelta(days=3)
            ),
            Vulnerability(
                title="Missing Firewall Rules",
                description="Unnecessary ports exposed to internet",
                severity=VulnerabilitySeverity.HIGH,
                cvss_score=7.2,
                cve_id="CVE-2024-0004",
                asset_id=assets[3].id,
                discovered_date=date.today() - timedelta(days=7),
                status=VulnerabilityStatus.IN_PROGRESS,
                mitigation_notes="Reviewing and updating firewall rules"
            ),
        ]
        db.add_all(vulnerabilities)
        db.commit()
        print(f"   ✓ Created {len(vulnerabilities)} vulnerabilities")
        
        # 6. Create Risks
        print("\n6. Creating risks...")
        risks = [
            Risk(
                title="Data Breach Risk - Production Server",
                description="High risk of data breach due to outdated SSL certificate",
                likelihood=3,
                impact=4,
                risk_score=12.0,
                risk_level=RiskLevel.MEDIUM,
                asset_id=assets[0].id,
                vulnerability_id=vulnerabilities[0].id,
                status=RiskStatus.IDENTIFIED,
                mitigation_plan="Renew SSL certificate and implement automated renewal monitoring"
            ),
            Risk(
                title="Critical SQL Injection Risk",
                description="Severe risk of database compromise through SQL injection",
                likelihood=4,
                impact=5,
                risk_score=20.0,
                risk_level=RiskLevel.CRITICAL,
                asset_id=assets[4].id,
                vulnerability_id=vulnerabilities[1].id,
                status=RiskStatus.MITIGATING,
                mitigation_plan="Immediate code review and implementation of prepared statements"
            ),
            Risk(
                title="System Compromise Risk",
                description="Risk of system compromise due to unpatched vulnerabilities",
                likelihood=4,
                impact=4,
                risk_score=16.0,
                risk_level=RiskLevel.HIGH,
                asset_id=assets[1].id,
                vulnerability_id=vulnerabilities[2].id,
                status=RiskStatus.ANALYZING,
                mitigation_plan="Schedule emergency patching during next maintenance window"
            ),
            Risk(
                title="Unauthorized Access Risk",
                description="Risk of unauthorized access through network exposure",
                likelihood=3,
                impact=4,
                risk_score=12.0,
                risk_level=RiskLevel.MEDIUM,
                asset_id=assets[3].id,
                vulnerability_id=vulnerabilities[4].id,
                status=RiskStatus.MITIGATING,
                mitigation_plan="Implement strict firewall rules and network segmentation"
            ),
            Risk(
                title="Backup Failure Risk",
                description="Risk of data loss if backup system fails",
                likelihood=2,
                impact=5,
                risk_score=10.0,
                risk_level=RiskLevel.MEDIUM,
                asset_id=assets[5].id,
                status=RiskStatus.MONITORED,
                mitigation_plan="Implement redundant backup systems and regular testing"
            ),
        ]
        db.add_all(risks)
        db.commit()
        print(f"   ✓ Created {len(risks)} risks")
        
        # 7. Create Notifications
        print("\n7. Creating notifications...")
        notifications = [
            Notification(
                user_id=users[0].id,
                title="Critical Vulnerability Detected",
                message="SQL injection vulnerability found in Customer Portal Application",
                type=NotificationType.ALERT,
                priority=NotificationPriority.URGENT,
                is_read=False
            ),
            Notification(
                user_id=users[1].id,
                title="New Asset Added",
                message="Backup Server has been added to the asset inventory",
                type=NotificationType.INFO,
                priority=NotificationPriority.LOW,
                is_read=False
            ),
            Notification(
                user_id=users[0].id,
                title="Risk Assessment Complete",
                message="Risk assessment for Production Web Server has been completed",
                type=NotificationType.SUCCESS,
                priority=NotificationPriority.MEDIUM,
                is_read=True,
                read_at=datetime.utcnow() - timedelta(hours=2)
            ),
            Notification(
                user_id=users[1].id,
                title="Patch Management Required",
                message="Critical security patches available for Database Server",
                type=NotificationType.WARNING,
                priority=NotificationPriority.HIGH,
                is_read=False
            ),
        ]
        db.add_all(notifications)
        db.commit()
        print(f"   ✓ Created {len(notifications)} notifications")
        
        # 8. Create Audit Logs
        print("\n8. Creating audit logs...")
        audit_logs = [
            AuditLog(
                user_id=users[0].id,
                action="CREATE",
                entity_type="Asset",
                entity_id=assets[0].id,
                details="Created Production Web Server asset",
                ip_address="192.168.1.50",
                user_agent="Mozilla/5.0"
            ),
            AuditLog(
                user_id=users[1].id,
                action="UPDATE",
                entity_type="Vulnerability",
                entity_id=vulnerabilities[1].id,
                details="Updated SQL Injection vulnerability status to IN_PROGRESS",
                ip_address="192.168.1.51",
                user_agent="Mozilla/5.0"
            ),
            AuditLog(
                user_id=users[0].id,
                action="CREATE",
                entity_type="Risk",
                entity_id=risks[1].id,
                details="Created Critical SQL Injection Risk",
                ip_address="192.168.1.50",
                user_agent="Mozilla/5.0"
            ),
        ]
        db.add_all(audit_logs)
        db.commit()
        print(f"   ✓ Created {len(audit_logs)} audit logs")
        
        print("\n" + "=" * 60)
        print("✓ Sample data created successfully!")
        print("=" * 60)
        print("\nSummary:")
        print(f"  - Organizations: 1")
        print(f"  - Departments: {len(departments)}")
        print(f"  - Users: {len(users)}")
        print(f"  - Assets: {len(assets)}")
        print(f"  - Vulnerabilities: {len(vulnerabilities)}")
        print(f"  - Risks: {len(risks)}")
        print(f"  - Notifications: {len(notifications)}")
        print(f"  - Audit Logs: {len(audit_logs)}")
        print("\nTest Credentials:")
        print("  Admin: admin@techcorp.com / Admin123!")
        print("  Manager: manager@techcorp.com / Manager123!")
        print("  Employee: john.doe@techcorp.com / Employee123!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Asset & Risk Management System - Database Seeding")
    print("=" * 60)
    
    response = input("\nThis will create sample data in the database. Continue? (y/n): ")
    
    if response.lower() == 'y':
        create_sample_data()
    else:
        print("Operation cancelled.")
