"""
Asset Model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class AssetCategory(str, enum.Enum):
    """Asset categories"""
    SERVER = "server"
    WORKSTATION = "workstation"
    NETWORK_DEVICE = "network_device"
    DATABASE = "database"
    APPLICATION = "application"
    MOBILE_DEVICE = "mobile_device"
    IOT_DEVICE = "iot_device"
    OTHER = "other"


class CriticalityLevel(str, enum.Enum):
    """Asset criticality levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AssetStatus(str, enum.Enum):
    """Asset status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"


class Asset(Base):
    """Asset model"""
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    category = Column(Enum(AssetCategory), nullable=False)
    criticality_level = Column(Enum(CriticalityLevel), default=CriticalityLevel.MEDIUM)
    status = Column(Enum(AssetStatus), default=AssetStatus.ACTIVE)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    location = Column(String, nullable=True)
    purchase_date = Column(Date, nullable=True)
    value = Column(Float, nullable=True)
    
    ip_address = Column(String, nullable=True)
    mac_address = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="assets")
    department = relationship("Department", back_populates="assets")
    vulnerabilities = relationship("Vulnerability", back_populates="asset")
    risks = relationship("Risk", back_populates="asset")
    
    def __repr__(self):
        return f"<Asset {self.name}>"
