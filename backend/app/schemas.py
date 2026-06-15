"""
Pydantic 数据模型（用于API请求/响应）
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==================== 品牌相关 ====================

class BrandBase(BaseModel):
    """品牌基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="品牌名称")
    search_keywords: Optional[str] = Field(None, description="搜索关键词")
    category: Optional[str] = Field(None, description="品类分类")
    is_active: bool = Field(True, description="是否启用监测")


class BrandCreate(BrandBase):
    """创建品牌请求"""
    pass


class BrandUpdate(BaseModel):
    """更新品牌请求"""
    name: Optional[str] = None
    search_keywords: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class BrandResponse(BrandBase):
    """品牌响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== 新闻相关 ====================

class NewsArticleBase(BaseModel):
    """新闻基础模型"""
    title: str = Field(..., description="标题")
    content: Optional[str] = Field(None, description="内容摘要")
    url: str = Field(..., description="原文链接")
    source: Optional[str] = Field(None, description="来源网站")
    source_type: str = Field("news", description="来源类型")
    published_at: Optional[datetime] = Field(None, description="发布时间")
    brand_id: int = Field(..., description="品牌ID")
    brand_name: Optional[str] = Field(None, description="品牌名称")


class NewsArticleCreate(NewsArticleBase):
    """创建新闻请求"""
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    heat_score: Optional[float] = None


class NewsArticleResponse(NewsArticleBase):
    """新闻响应模型"""
    id: int
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    heat_score: float = 0
    is_top_news: bool = False
    is_notified: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 搜索相关 ====================

class SearchRequest(BaseModel):
    """搜索请求"""
    keyword: str = Field(..., min_length=1, description="搜索关键词")
    days: Optional[int] = Field(7, ge=1, le=30, description="搜索最近几天")
    limit: Optional[int] = Field(20, ge=1, le=100, description="返回数量")


class SearchResponse(BaseModel):
    """搜索响应"""
    keyword: str
    total: int
    articles: List[NewsArticleResponse]


# ==================== 展板相关 ====================

class DashboardStats(BaseModel):
    """展板统计数据"""
    total_brands: int
    total_news_today: int
    negative_news_count: int
    top_brands: List[dict]


class DailyTopNewsResponse(BaseModel):
    """每日Top新闻响应"""
    date: str
    brand_name: str
    title: str
    url: str
    sentiment_label: Optional[str]
    heat_score: Optional[float]
    rank: int


# ==================== 通用响应 ====================

class APIResponse(BaseModel):
    """通用API响应"""
    success: bool = True
    message: str = ""
    data: Optional[dict] = None
