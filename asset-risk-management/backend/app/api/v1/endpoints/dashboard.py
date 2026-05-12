"""
Dashboard Analytics Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.asset import Asset, CriticalityLevel
from app.models.vulnerability import Vulnerability, VulnerabilitySeverity
from app.models.risk import Risk, RiskLevel
from app.models.audit_log import AuditLog

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics
    """
    # Count totals
    total_assets = db.query(Asset).count()
    total_vulnerabilities = db.query(Vulnerability).count()
    total_risks = db.query(Risk).count()
    total_users = db.query(User).filter(User.is_active == True).count()
    
    # Count critical items
    critical_assets = db.query(Asset).filter(
        Asset.criticality_level == CriticalityLevel.CRITICAL
    ).count()
    
    critical_vulnerabilities = db.query(Vulnerability).filter(
        Vulnerability.severity == VulnerabilitySeverity.CRITICAL
    ).count()
    
    critical_risks = db.query(Risk).filter(
        Risk.risk_level == RiskLevel.CRITICAL
    ).count()
    
    return {
        "total_assets": total_assets,
        "total_vulnerabilities": total_vulnerabilities,
        "total_risks": total_risks,
        "total_users": total_users,
        "critical_assets": critical_assets,
        "critical_vulnerabilities": critical_vulnerabilities,
        "critical_risks": critical_risks
    }


@router.get("/risk-distribution")
async def get_risk_distribution(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get risk distribution by level
    """
    risk_distribution = db.query(
        Risk.risk_level,
        func.count(Risk.id).label('count')
    ).group_by(Risk.risk_level).all()
    
    return [
        {"level": level.value, "count": count}
        for level, count in risk_distribution
    ]


@router.get("/asset-criticality")
async def get_asset_criticality_distribution(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get asset distribution by criticality level
    """
    asset_distribution = db.query(
        Asset.criticality_level,
        func.count(Asset.id).label('count')
    ).group_by(Asset.criticality_level).all()
    
    return [
        {"level": level.value, "count": count}
        for level, count in asset_distribution
    ]


@router.get("/vulnerability-severity")
async def get_vulnerability_severity_distribution(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get vulnerability distribution by severity
    """
    vuln_distribution = db.query(
        Vulnerability.severity,
        func.count(Vulnerability.id).label('count')
    ).group_by(Vulnerability.severity).all()
    
    return [
        {"severity": severity.value, "count": count}
        for severity, count in vuln_distribution
    ]


@router.get("/recent-activities")
async def get_recent_activities(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get recent audit log activities
    """
    activities = db.query(AuditLog).order_by(
        AuditLog.created_at.desc()
    ).limit(10).all()
    
    return [
        {
            "id": activity.id,
            "user_id": activity.user_id,
            "action": activity.action,
            "entity_type": activity.entity_type,
            "entity_id": activity.entity_id,
            "details": activity.details,
            "created_at": activity.created_at
        }
        for activity in activities
    ]


@router.get("/critical-assets")
async def get_critical_assets(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get critical assets with their risk count
    """
    critical_assets = db.query(Asset).filter(
        Asset.criticality_level == CriticalityLevel.CRITICAL
    ).limit(10).all()
    
    result = []
    for asset in critical_assets:
        risk_count = db.query(Risk).filter(Risk.asset_id == asset.id).count()
        vuln_count = db.query(Vulnerability).filter(
            Vulnerability.asset_id == asset.id
        ).count()
        
        result.append({
            "id": asset.id,
            "name": asset.name,
            "category": asset.category.value,
            "criticality_level": asset.criticality_level.value,
            "risk_count": risk_count,
            "vulnerability_count": vuln_count
        })
    
    return result
