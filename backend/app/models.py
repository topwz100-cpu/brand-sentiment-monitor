"""
数据库模型定义
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Brand(Base):
    """品牌表"""
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)  # 品牌名称
    search_keywords = Column(String(500))  # 搜索关键词（多个用逗号分隔）
    category = Column(String(50))  # 品类分类
    is_active = Column(Boolean, default=True)  # 是否启用监测
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Brand(name='{self.name}')>"


class NewsArticle(Base):
    """新闻文章表"""
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)  # 标题
    content = Column(Text)  # 内容摘要
    url = Column(String(1000), nullable=False)  # 原文链接
    source = Column(String(100))  # 来源网站
    source_type = Column(String(20), default="news")  # 来源类型: news/weibo
    published_at = Column(DateTime)  # 发布时间
    
    # 关联品牌
    brand_id = Column(Integer, nullable=False)  # 关联的品牌ID
    brand_name = Column(String(100))  # 品牌名称（冗余存储）
    
    # 情感分析
    sentiment_score = Column(Float)  # 情感分数: 0-1 (0负面, 1正面)
    sentiment_label = Column(String(10))  # 标签: positive/negative/neutral
    
    # 热度指标
    heat_score = Column(Float, default=0)  # 热度分数
    is_top_news = Column(Boolean, default=False)  # 是否Top新闻
    
    # 状态
    is_notified = Column(Boolean, default=False)  # 是否已通知
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<NewsArticle(title='{self.title[:50]}...')>"


class DailyTopNews(Base):
    """每日Top新闻表"""
    __tablename__ = "daily_top_news"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(10), index=True, nullable=False)  # 日期: YYYY-MM-DD
    brand_id = Column(Integer, nullable=False)
    brand_name = Column(String(100))
    news_id = Column(Integer, nullable=False)  # 关联的新闻ID
    rank = Column(Integer, nullable=False)  # 排名
    heat_score = Column(Float)
    
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<DailyTopNews(date='{self.date}', rank={self.rank})>"


class SearchLog(Base):
    """搜索日志表"""
    __tablename__ = "search_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(200), nullable=False)  # 搜索关键词
    results_count = Column(Integer, default=0)  # 结果数量
    search_time = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<SearchLog(keyword='{self.keyword}')>"


# 创建索引
Index('idx_news_brand_date', NewsArticle.brand_id, NewsArticle.published_at)
Index('idx_news_sentiment', NewsArticle.sentiment_label)
Index('idx_news_heat', NewsArticle.heat_score.desc())
Index('idx_topnews_date', DailyTopNews.date)
