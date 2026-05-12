"""
Risk Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    """Risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskStatus(str, Enum):
    """Risk status"""
    IDENTIFIED = "identified"
    ANALYZING = "analyzing"
    MITIGATING = "mitigating"
    MONITORED = "monitored"
    CLOSED = "closed"


class RiskBase(BaseModel):
    """Base risk schema"""
    title: str
    description: Optional[str] = None
    likelihood: int = Field(..., ge=1, le=5)
    impact: int = Field(..., ge=1, le=5)


class RiskCreate(RiskBase):
    """Risk creation schema"""
    asset_id: int
    vulnerability_id: Optional[int] = None
    mitigation_plan: Optional[str] = None


class RiskUpdate(BaseModel):
    """Risk update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    likelihood: Optional[int] = Field(None, ge=1, le=5)
    impact: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[RiskStatus] = None
    mitigation_plan: Optional[str] = None


class RiskResponse(RiskBase):
    """Risk response schema"""
    id: int
    risk_score: float
    risk_level: RiskLevel
    asset_id: int
    vulnerability_id: Optional[int]
    status: RiskStatus
    mitigation_plan: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RiskListResponse(BaseModel):
    """Risk list response with pagination"""
    total: int
    items: list[RiskResponse]
    page: int
    page_size: int


class RiskCalculation(BaseModel):
    """Risk calculation request"""
    likelihood: int = Field(..., ge=1, le=5)
    impact: int = Field(..., ge=1, le=5)


class RiskCalculationResponse(BaseModel):
    """Risk calculation response"""
    likelihood: int
    impact: int
    risk_score: float
    risk_level: RiskLevel
