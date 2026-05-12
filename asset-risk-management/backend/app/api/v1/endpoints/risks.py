"""
Risk Management Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.risk import Risk, RiskLevel, RiskStatus
from app.schemas.risk import (
    RiskCreate, RiskUpdate, RiskResponse, RiskListResponse,
    RiskCalculation, RiskCalculationResponse
)

router = APIRouter()


def calculate_risk_score(likelihood: int, impact: int) -> tuple[float, RiskLevel]:
    """
    Calculate risk score and level based on likelihood and impact
    Risk Score = Likelihood × Impact
    """
    risk_score = likelihood * impact
    
    # Determine risk level
    if risk_score <= 5:
        risk_level = RiskLevel.LOW
    elif risk_score <= 12:
        risk_level = RiskLevel.MEDIUM
    elif risk_score <= 20:
        risk_level = RiskLevel.HIGH
    else:
        risk_level = RiskLevel.CRITICAL
    
    return risk_score, risk_level


@router.get("/", response_model=RiskListResponse)
async def get_risks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    risk_level: Optional[RiskLevel] = None,
    status: Optional[RiskStatus] = None,
    asset_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all risks with filtering and pagination
    """
    query = db.query(Risk)
    
    # Apply filters
    if risk_level:
        query = query.filter(Risk.risk_level == risk_level)
    if status:
        query = query.filter(Risk.status == status)
    if asset_id:
        query = query.filter(Risk.asset_id == asset_id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    risks = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": risks,
        "page": skip // limit + 1,
        "page_size": limit
    }


@router.get("/calculate", response_model=RiskCalculationResponse)
async def calculate_risk(
    calculation: RiskCalculation = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """
    Calculate risk score and level
    """
    risk_score, risk_level = calculate_risk_score(
        calculation.likelihood,
        calculation.impact
    )
    
    return {
        "likelihood": calculation.likelihood,
        "impact": calculation.impact,
        "risk_score": risk_score,
        "risk_level": risk_level
    }


@router.get("/{risk_id}", response_model=RiskResponse)
async def get_risk(
    risk_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get risk by ID
    """
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    
    if not risk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk not found"
        )
    
    return risk


@router.post("/", response_model=RiskResponse, status_code=status.HTTP_201_CREATED)
async def create_risk(
    risk_data: RiskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new risk
    """
    # Calculate risk score and level
    risk_score, risk_level = calculate_risk_score(
        risk_data.likelihood,
        risk_data.impact
    )
    
    new_risk = Risk(
        **risk_data.dict(),
        risk_score=risk_score,
        risk_level=risk_level
    )
    
    db.add(new_risk)
    db.commit()
    db.refresh(new_risk)
    
    return new_risk


@router.put("/{risk_id}", response_model=RiskResponse)
async def update_risk(
    risk_id: int,
    risk_update: RiskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update risk by ID
    """
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    
    if not risk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk not found"
        )
    
    # Update risk fields
    update_data = risk_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(risk, field, value)
    
    # Recalculate risk score if likelihood or impact changed
    if 'likelihood' in update_data or 'impact' in update_data:
        risk_score, risk_level = calculate_risk_score(risk.likelihood, risk.impact)
        risk.risk_score = risk_score
        risk.risk_level = risk_level
    
    db.commit()
    db.refresh(risk)
    
    return risk


@router.delete("/{risk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_risk(
    risk_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete risk by ID
    """
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    
    if not risk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk not found"
        )
    
    db.delete(risk)
    db.commit()
    
    return None
