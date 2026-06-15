"""
新闻搜索API路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List
from datetime import datetime, timedelta

from ..database import get_db
from ..models import NewsArticle, Brand
from ..schemas import SearchRequest, SearchResponse, NewsArticleResponse
from ..services.search import search_service
from ..services.sentiment import sentiment_service

router = APIRouter(prefix="/news", tags=["新闻搜索"])


@router.get("/search", response_model=SearchResponse)
async def search_news(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    days: int = Query(7, ge=1, le=30, description="搜索最近几天"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
    db: Session = Depends(get_db)
):
    """
    搜索新闻
    
    Args:
        keyword: 搜索关键词
        days: 搜索最近几天的数据
        limit: 返回数量
        
    Returns:
        搜索结果
    """
    try:
        # 调用搜索服务
        results = await search_service.search_brand(keyword, days)
        
        # 限制数量
        results = results[:limit]
        
        # 转换为响应模型
        articles = []
        for item in results:
            article = NewsArticleResponse(
                id=0,  # 临时ID
                title=item["title"],
                content=item.get("content", ""),
                url=item["url"],
                source=item.get("source", ""),
                source_type=item.get("source_type", "news"),
                published_at=item.get("published_at"),
                brand_id=0,
                brand_name=keyword,
                sentiment_score=None,
                sentiment_label=None,
                heat_score=0,
                is_top_news=False,
                is_notified=False,
                created_at=datetime.now()
            )
            articles.append(article)
            
        return SearchResponse(
            keyword=keyword,
            total=len(articles),
            articles=articles
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@router.get("/brand/{brand_id}", response_model=List[NewsArticleResponse])
def get_brand_news(
    brand_id: int,
    days: int = Query(7, ge=1, le=30),
    sentiment: Optional[str] = Query(None, description="情感筛选: positive/negative/neutral"),
    db: Session = Depends(get_db)
):
    """
    获取品牌相关新闻
    
    Args:
        brand_id: 品牌ID
        days: 最近几天
        sentiment: 情感筛选
        
    Returns:
        新闻列表
    """
    # 检查品牌是否存在
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    
    # 构建查询
    cutoff_date = datetime.now() - timedelta(days=days)
    query = db.query(NewsArticle).filter(
        and_(
            NewsArticle.brand_id == brand_id,
            NewsArticle.published_at >= cutoff_date
        )
    )
    
    # 情感筛选
    if sentiment:
        query = query.filter(NewsArticle.sentiment_label == sentiment)
        
    # 排序
    news = query.order_by(NewsArticle.published_at.desc()).all()
    
    return news


@router.get("/latest", response_model=List[NewsArticleResponse])
def get_latest_news(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    获取最新新闻
    
    Args:
        limit: 返回数量
        
    Returns:
        最新新闻列表
    """
    news = db.query(NewsArticle).order_by(
        NewsArticle.published_at.desc()
    ).limit(limit).all()
    
    return news


@router.get("/negative", response_model=List[NewsArticleResponse])
def get_negative_news(
    days: int = Query(7, ge=1, le=30),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    获取负面新闻
    
    Args:
        days: 最近几天
        limit: 返回数量
        
    Returns:
        负面新闻列表
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    news = db.query(NewsArticle).filter(
        and_(
            NewsArticle.sentiment_label == "negative",
            NewsArticle.published_at >= cutoff_date
        )
    ).order_by(
        NewsArticle.published_at.desc()
    ).limit(limit).all()
    
    return news
