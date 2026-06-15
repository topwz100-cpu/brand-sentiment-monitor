"""
大客户舆情监测系统 - 配置文件
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "大客户舆情监测系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sentiment.db")
    
    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Tavily API配置
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "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")
    
    # 钉钉机器人配置
    DINGTALK_WEBHOOK: str = os.getenv("DINGTALK_WEBHOOK", "https://oapi.dingtalk.com/robot/send?access_token=012c450ba7bc70b21033e56268f0c39398fac9189d22df6a87168cd1249220f8")
    
    # 搜索配置
    SEARCH_MAX_RESULTS: int = 50  # 每次搜索最大结果数
    SEARCH_DAYS: int = 1  # 搜索最近几天的数据
    
    # 定时任务配置
    DAILY_UPDATE_HOUR: int = 6  # 每天几点更新 (凌晨6点)
    DAILY_UPDATE_MINUTE: int = 0
    
    # 舆情预警配置
    NEGATIVE_THRESHOLD: float = 0.3  # 负面情感阈值
    TOP_N_BRANDS: int = 20  # Top20品牌
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"


# 全局配置实例
settings = Settings()
