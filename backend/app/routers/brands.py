"""
品牌管理API路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import Brand
from ..schemas import BrandCreate, BrandUpdate, BrandResponse

router = APIRouter(prefix="/brands", tags=["品牌管理"])


@router.get("/", response_model=List[BrandResponse])
def get_brands(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    获取品牌列表
    
    Args:
        skip: 跳过数量
        limit: 返回数量
        is_active: 是否只返回活跃品牌
        
    Returns:
        品牌列表
    """
    query = db.query(Brand)
    
    if is_active is not None:
        query = query.filter(Brand.is_active == is_active)
        
    brands = query.offset(skip).limit(limit).all()
    return brands


@router.get("/{brand_id}", response_model=BrandResponse)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    """
    获取单个品牌详情
    
    Args:
        brand_id: 品牌ID
        
    Returns:
        品牌详情
    """
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    return brand


@router.post("/", response_model=BrandResponse)
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    """
    创建品牌
    
    Args:
        brand: 品牌信息
        
    Returns:
        创建的品牌
    """
    # 检查品牌是否已存在
    existing = db.query(Brand).filter(Brand.name == brand.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="品牌已存在")
    
    db_brand = Brand(**brand.dict())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


@router.put("/{brand_id}", response_model=BrandResponse)
def update_brand(brand_id: int, brand_update: BrandUpdate, db: Session = Depends(get_db)):
    """
    更新品牌信息
    
    Args:
        brand_id: 品牌ID
        brand_update: 更新内容
        
    Returns:
        更新后的品牌
    """
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    
    # 更新字段
    update_data = brand_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(brand, field, value)
        
    db.commit()
    db.refresh(brand)
    return brand


@router.delete("/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    """
    删除品牌（软删除：设置为不活跃）
    
    Args:
        brand_id: 品牌ID
        
    Returns:
        操作结果
    """
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    
    # 软删除
    brand.is_active = False
    db.commit()
    
    return {"success": True, "message": "品牌已删除"}


@router.post("/batch-import")
def batch_import_brands(brand_names: List[str], db: Session = Depends(get_db)):
    """
    批量导入品牌
    
    Args:
        brand_names: 品牌名称列表
        
    Returns:
        导入结果
    """
    imported = 0
    skipped = 0
    
    for name in brand_names:
        # 去重检查
        existing = db.query(Brand).filter(Brand.name == name).first()
        if existing:
            skipped += 1
            continue
            
        brand = Brand(name=name, is_active=True)
        db.add(brand)
        imported += 1
        
    db.commit()
    
    return {
        "success": True,
        "imported": imported,
        "skipped": skipped,
        "message": f"成功导入 {imported} 个品牌，跳过 {skipped} 个重复品牌"
    }
