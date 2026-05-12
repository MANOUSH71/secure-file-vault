"""
Vulnerability Management Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.vulnerability import Vulnerability, VulnerabilitySeverity, VulnerabilityStatus
from app.schemas.vulnerability import (
    VulnerabilityCreate, VulnerabilityUpdate, VulnerabilityResponse, VulnerabilityListResponse
)

router = APIRouter()


@router.get("/", response_model=VulnerabilityListResponse)
async def get_vulnerabilities(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    severity: Optional[VulnerabilitySeverity] = None,
    status: Optional[VulnerabilityStatus] = None,
    asset_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all vulnerabilities with filtering and pagination
    """
    query = db.query(Vulnerability)
    
    # Apply filters
    if severity:
        query = query.filter(Vulnerability.severity == severity)
    if status:
        query = query.filter(Vulnerability.status == status)
    if asset_id:
        query = query.filter(Vulnerability.asset_id == asset_id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    vulnerabilities = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": vulnerabilities,
        "page": skip // limit + 1,
        "page_size": limit
    }


@router.get("/asset/{asset_id}", response_model=List[VulnerabilityResponse])
async def get_vulnerabilities_by_asset(
    asset_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all vulnerabilities for a specific asset
    """
    vulnerabilities = db.query(Vulnerability).filter(
        Vulnerability.asset_id == asset_id
    ).all()
    
    return vulnerabilities


@router.get("/{vulnerability_id}", response_model=VulnerabilityResponse)
async def get_vulnerability(
    vulnerability_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get vulnerability by ID
    """
    vulnerability = db.query(Vulnerability).filter(
        Vulnerability.id == vulnerability_id
    ).first()
    
    if not vulnerability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vulnerability not found"
        )
    
    return vulnerability


@router.post("/", response_model=VulnerabilityResponse, status_code=status.HTTP_201_CREATED)
async def create_vulnerability(
    vulnerability_data: VulnerabilityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new vulnerability
    """
    new_vulnerability = Vulnerability(**vulnerability_data.dict())
    
    db.add(new_vulnerability)
    db.commit()
    db.refresh(new_vulnerability)
    
    return new_vulnerability


@router.put("/{vulnerability_id}", response_model=VulnerabilityResponse)
async def update_vulnerability(
    vulnerability_id: int,
    vulnerability_update: VulnerabilityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update vulnerability by ID
    """
    vulnerability = db.query(Vulnerability).filter(
        Vulnerability.id == vulnerability_id
    ).first()
    
    if not vulnerability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vulnerability not found"
        )
    
    # Update vulnerability fields
    update_data = vulnerability_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(vulnerability, field, value)
    
    db.commit()
    db.refresh(vulnerability)
    
    return vulnerability


@router.delete("/{vulnerability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vulnerability(
    vulnerability_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete vulnerability by ID
    """
    vulnerability = db.query(Vulnerability).filter(
        Vulnerability.id == vulnerability_id
    ).first()
    
    if not vulnerability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vulnerability not found"
        )
    
    db.delete(vulnerability)
    db.commit()
    
    return None
