"""
Asset Management Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.asset import Asset, AssetCategory, CriticalityLevel, AssetStatus
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse, AssetListResponse

router = APIRouter()


@router.get("/", response_model=AssetListResponse)
async def get_assets(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[AssetCategory] = None,
    criticality: Optional[CriticalityLevel] = None,
    status: Optional[AssetStatus] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all assets with filtering and pagination
    """
    query = db.query(Asset)
    
    # Apply filters
    if category:
        query = query.filter(Asset.category == category)
    if criticality:
        query = query.filter(Asset.criticality_level == criticality)
    if status:
        query = query.filter(Asset.status == status)
    if search:
        query = query.filter(Asset.name.ilike(f"%{search}%"))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    assets = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": assets,
        "page": skip // limit + 1,
        "page_size": limit
    }


@router.get("/categories", response_model=List[str])
async def get_asset_categories(current_user: User = Depends(get_current_active_user)):
    """
    Get all asset categories
    """
    return [category.value for category in AssetCategory]


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get asset by ID
    """
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    return asset


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_data: AssetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new asset
    """
    new_asset = Asset(**asset_data.dict())
    
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    
    return new_asset


@router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: int,
    asset_update: AssetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update asset by ID
    """
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    # Update asset fields
    update_data = asset_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(asset, field, value)
    
    db.commit()
    db.refresh(asset)
    
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete asset by ID
    """
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    db.delete(asset)
    db.commit()
    
    return None


@router.get("/search/", response_model=List[AssetResponse])
async def search_assets(
    q: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search assets by name or description
    """
    assets = db.query(Asset).filter(
        (Asset.name.ilike(f"%{q}%")) | (Asset.description.ilike(f"%{q}%"))
    ).limit(20).all()
    
    return assets
