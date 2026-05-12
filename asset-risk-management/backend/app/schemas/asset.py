"""
Asset Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class AssetCategory(str, Enum):
    """Asset categories"""
    SERVER = "server"
    WORKSTATION = "workstation"
    NETWORK_DEVICE = "network_device"
    DATABASE = "database"
    APPLICATION = "application"
    MOBILE_DEVICE = "mobile_device"
    IOT_DEVICE = "iot_device"
    OTHER = "other"


class CriticalityLevel(str, Enum):
    """Asset criticality levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AssetStatus(str, Enum):
    """Asset status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"


class AssetBase(BaseModel):
    """Base asset schema"""
    name: str
    description: Optional[str] = None
    category: AssetCategory
    criticality_level: CriticalityLevel = CriticalityLevel.MEDIUM
    status: AssetStatus = AssetStatus.ACTIVE
    location: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    serial_number: Optional[str] = None


class AssetCreate(AssetBase):
    """Asset creation schema"""
    owner_id: Optional[int] = None
    department_id: Optional[int] = None
    purchase_date: Optional[date] = None
    value: Optional[float] = None


class AssetUpdate(BaseModel):
    """Asset update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[AssetCategory] = None
    criticality_level: Optional[CriticalityLevel] = None
    status: Optional[AssetStatus] = None
    owner_id: Optional[int] = None
    department_id: Optional[int] = None
    location: Optional[str] = None
    purchase_date: Optional[date] = None
    value: Optional[float] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    serial_number: Optional[str] = None


class AssetResponse(AssetBase):
    """Asset response schema"""
    id: int
    owner_id: Optional[int]
    department_id: Optional[int]
    purchase_date: Optional[date]
    value: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AssetListResponse(BaseModel):
    """Asset list response with pagination"""
    total: int
    items: list[AssetResponse]
    page: int
    page_size: int
