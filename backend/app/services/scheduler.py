"""
定时任务调度器
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import asyncio
from typing import List

from ..database import SessionLocal
from ..models import Brand, NewsArticle, DailyTopNews
from ..config import settings
from .search import search_service
from .sentiment import sentiment_service
from .dingtalk import dingtalk_service


class SchedulerService:
    """定时任务服务"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        
    def start(self):
        """启动定时任务"""
        # 每天凌晨6点执行数据更新
        self.scheduler.add_job(
            self.daily_update,
            CronTrigger(hour=settings.DAILY_UPDATE_HOUR, minute=settings.DAILY_UPDATE_MINUTE),
            id="daily_update",
            replace_existing=True
        )
        
        self.scheduler.start()
        print(f"定时任务已启动，每天 {settings.DAILY_UPDATE_HOUR}:{settings.DAILY_UPDATE_MINUTE:02d} 执行更新")
        
    def stop(self):
        """停止定时任务"""
        self.scheduler.shutdown()
        
    def daily_update(self):
        """
        每日更新任务：
        1. 获取所有活跃品牌
        2. 搜索每个品牌的最新资讯
        3. 进行情感分析
        4. 计算热度分数
        5. 生成Top20
        6. 发送钉钉通知
        """
        print(f"开始执行每日更新任务: {datetime.now()}")
        
        try:
            # 创建数据库会话
            db = SessionLocal()
            
            # 获取所有活跃品牌
            brands = db.query(Brand).filter(Brand.is_active == True).all()
            print(f"共 {len(brands)} 个品牌需要监测")
            
            # 收集所有新闻
            all_news = []
            
            for brand in brands:
                try:
                    # 搜索品牌资讯
                    news_list = asyncio.run(search_service.search_brand(brand.name, days=1))
                    
                    for news in news_list:
                        # 情感分析
                        sentiment = sentiment_service.analyze(news.get("content", ""))
                        
                        # 创建新闻记录
                        article = NewsArticle(
                            title=news["title"],
                            content=news.get("content", ""),
                            url=news["url"],
                            source=news.get("source", ""),
                            source_type=news.get("source_type", "news"),
                            published_at=news.get("published_at"),
                            brand_id=brand.id,
                            brand_name=brand.name,
                            sentiment_score=sentiment["score"],
                            sentiment_label=sentiment["label"]
                        )
                        
                        db.add(article)
                        all_news.append(article)
                        
                        # 负面预警
                        if sentiment["label"] == "negative" and sentiment["score"] < settings.NEGATIVE_THRESHOLD:
                            asyncio.run(dingtalk_service.send_negative_alert(
                                brand_name=brand.name,
                                news_title=news["title"],
                                news_url=news["url"],
                                sentiment_score=sentiment["score"]
                            ))
                            
                except Exception as e:
                    print(f"品牌 {brand.name} 搜索失败: {e}")
                    continue
            
            # 提交所有新闻
            db.commit()
            
            # 计算热度分数并排序
            for news in all_news:
                news.heat_score = self._calculate_heat(news)
                
            # 排序并取Top20
            all_news.sort(key=lambda x: x.heat_score, reverse=True)
            top_20 = all_news[:20]
            
            # 标记Top新闻
            for news in top_20:
                news.is_top_news = True
                
            # 保存Top20记录
            today = datetime.now().strftime("%Y-%m-%d")
            for i, news in enumerate(top_20, 1):
                top_record = DailyTopNews(
                    date=today,
                    brand_id=news.brand_id,
                    brand_name=news.brand_name,
                    news_id=news.id,
                    rank=i,
                    heat_score=news.heat_score
                )
                db.add(top_record)
                
            db.commit()
            
            # 发送每日摘要
            top_news_data = [
                {
                    "brand_name": news.brand_name,
                    "title": news.title,
                    "url": news.url,
                    "sentiment_label": news.sentiment_label,
                    "heat_score": news.heat_score
                }
                for news in top_20
            ]
            
            asyncio.run(dingtalk_service.send_daily_summary(today, top_news_data))
            
            print(f"每日更新任务完成: {datetime.now()}")
            
        except Exception as e:
            print(f"每日更新任务失败: {e}")
            
        finally:
            db.close()
            
    def _calculate_heat(self, news: NewsArticle) -> float:
        """
        计算新闻热度分数
        
        算法：
        - 时间衰减：越新的新闻分数越高
        - 情感权重：负面新闻权重更高（需要关注）
        - 来源权重：权威媒体权重更高
        """
        import time
        
        # 时间衰减因子 (0-1)
        if news.published_at:
            hours_ago = (datetime.now() - news.published_at).total_seconds() / 3600
            time_factor = max(0, 1 - (hours_ago / 24))  # 24小时内线性衰减
        else:
            time_factor = 0.5
            
        # 情感因子 (负面新闻权重更高)
        if news.sentiment_label == "negative":
            sentiment_factor = 1.5
        elif news.sentiment_label == "positive":
            sentiment_factor = 1.0
        else:
            sentiment_factor = 0.8
            
        # 来源权重
        source_weights = {
            "新浪": 1.2,
            "腾讯": 1.2,
            "网易": 1.1,
            "搜狐": 1.1,
            "微博": 1.0,
            "default": 1.0
        }
        source_factor = source_weights.get(news.source, source_weights["default"])
        
        # 综合热度分数
        heat_score = time_factor * sentiment_factor * source_factor * 100
        
        return round(heat_score, 2)


# 全局定时任务服务实例
scheduler_service = SchedulerService()
