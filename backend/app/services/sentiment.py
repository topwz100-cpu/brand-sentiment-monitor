"""
情感分析服务
使用SnowNLP进行中文情感分析
"""
from snownlp import SnowNLP
from typing import Dict, Optional
import jieba


class SentimentService:
    """情感分析服务"""
    
    def __init__(self):
        # 加载自定义词典（可选）
        # jieba.load_userdict("custom_dict.txt")
        pass
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        分析文本情感
        
        Args:
            text: 待分析文本
            
        Returns:
            {
                "score": float,  # 0-1, 越接近1越正面
                "label": str,   # positive/negative/neutral
                "confidence": float  # 置信度
            }
        """
        if not text or len(text.strip()) == 0:
            return {
                "score": 0.5,
                "label": "neutral",
                "confidence": 0.0
            }
        
        try:
            # 使用SnowNLP进行情感分析
            s = SnowNLP(text)
            sentiment_score = s.sentiments  # 0-1
            
            # 判断情感标签
            if sentiment_score > 0.6:
                label = "positive"
                confidence = sentiment_score
            elif sentiment_score < 0.4:
                label = "negative"
                confidence = 1 - sentiment_score
            else:
                label = "neutral"
                confidence = 0.5
            
            return {
                "score": sentiment_score,
                "label": label,
                "confidence": confidence
            }
            
        except Exception as e:
            print(f"情感分析失败: {e}")
            return {
                "score": 0.5,
                "label": "neutral",
                "confidence": 0.0
            }
    
    def analyze_batch(self, texts: list) -> list:
        """
        批量分析文本情感
        
        Args:
            texts: 文本列表
            
        Returns:
            情感分析结果列表
        """
        results = []
        for text in texts:
            result = self.analyze(text)
            results.append(result)
        return results
    
    def is_negative(self, text: str, threshold: float = 0.3) -> bool:
        """
        判断是否为负面舆情
        
        Args:
            text: 文本内容
            threshold: 负面阈值
            
        Returns:
            是否为负面
        """
        result = self.analyze(text)
        return result["score"] < threshold


# 全局情感分析服务实例
sentiment_service = SentimentService()
