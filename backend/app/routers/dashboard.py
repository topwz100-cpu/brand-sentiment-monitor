"""
展板数据API路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List
from datetime import datetime, timedelta

from ..database import get_db
from ..models import NewsArticle, DailyTopNews, Brand
from ..schemas import DailyTopNewsResponse, DashboardStats

router = APIRouter(prefix="/dashboard", tags=["展板数据"])


@router.get("/top20", response_model=List[dict])
def get_top20_news(
    date: Optional[str] = Query(None, description="日期 (YYYY-MM-DD)，默认今天"),
    db: Session = Depends(get_db)
):
    """
    获取Top20热门新闻
    
    Args:
        date: 日期，默认今天
        
    Returns:
        Top20新闻列表
    """
    # 默认今天
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
        
    # 查询Top20
    top_news = db.query(DailyTopNews).filter(
        DailyTopNews.date == date
    ).order_by(DailyTopNews.rank).all()
    
    # 如果没有数据，返回空列表
    if not top_news:
        return []
    
    # 获取详细新闻信息
    result = []
    for item in top_news:
        news = db.query(NewsArticle).filter(NewsArticle.id == item.news_id).first()
        if news:
            result.append({
                "rank": item.rank,
                "brand_name": item.brand_name,
                "title": news.title,
                "content": news.content,
                "url": news.url,
                "source": news.source,
                "published_at": news.published_at,
                "sentiment_label": news.sentiment_label,
                "sentiment_score": news.sentiment_score,
                "heat_score": item.heat_score
            })
            
    return result


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    获取展板统计数据
    
    Returns:
        统计数据
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 品牌总数
    total_brands = db.query(Brand).filter(Brand.is_active == True).count()
    
    # 今日新闻数
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    total_news_today = db.query(NewsArticle).filter(
        NewsArticle.created_at >= today_start
    ).count()
    
    # 负面新闻数
    negative_news = db.query(NewsArticle).filter(
        and_(
            NewsArticle.sentiment_label == "negative",
            NewsArticle.created_at >= today_start
        )
    ).count()
    
    # Top品牌（按新闻数量）
    top_brands_query = db.query(
        NewsArticle.brand_name,
        func.count(NewsArticle.id).label("news_count")
    ).filter(
        NewsArticle.created_at >= today_start
    ).group_by(
        NewsArticle.brand_name
    ).order_by(
        func.count(NewsArticle.id).desc()
    ).limit(10).all()
    
    top_brands = [
        {"name": brand_name, "count": count}
        for brand_name, count in top_brands_query
    ]
    
    return DashboardStats(
        total_brands=total_brands,
        total_news_today=total_news_today,
        negative_news_count=negative_news,
        top_brands=top_brands
    )


@router.get("/trends")
def get_sentiment_trends(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """
    获取情感趋势数据
    
    Args:
        days: 最近几天
        
    Returns:
        趋势数据
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # 按天统计
    daily_stats = db.query(
        func.date(NewsArticle.created_at).label("date"),
        NewsArticle.sentiment_label,
        func.count(NewsArticle.id).label("count")
    ).filter(
        NewsArticle.created_at >= cutoff_date
    ).group_by(
        func.date(NewsArticle.created_at),
        NewsArticle.sentiment_label
    ).all()
    
    # 整理数据
    trends = {}
    for date, sentiment, count in daily_stats:
        date_str = date.strftime("%Y-%m-%d")
        if date_str not in trends:
            trends[date_str] = {"positive": 0, "negative": 0, "neutral": 0}
        if sentiment in trends[date_str]:
            trends[date_str][sentiment] = count
            
    return trends


@router.get("/brand-distribution")
def get_brand_distribution(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """
    获取品牌新闻分布
    
    Args:
        days: 最近几天
        
    Returns:
        品牌分布数据
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    distribution = db.query(
        NewsArticle.brand_name,
        func.count(NewsArticle.id).label("count")
    ).filter(
        NewsArticle.created_at >= cutoff_date
    ).group_by(
        NewsArticle.brand_name
    ).order_by(
        func.count(NewsArticle.id).desc()
    ).all()
    
    return [
        {"name": brand_name, "value": count}
        for brand_name, count in distribution
    ]
