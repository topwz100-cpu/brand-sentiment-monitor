"""
钉钉通知服务
"""
import httpx
import json
from datetime import datetime
from typing import List, Dict
from ..config import settings


class DingTalkService:
    """钉钉通知服务"""
    
    def __init__(self):
        self.webhook_url = settings.DINGTALK_WEBHOOK
        
    async def send_text(self, content: str) -> bool:
        """
        发送文本消息
        
        Args:
            content: 消息内容
            
        Returns:
            是否发送成功
        """
        payload = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        
        return await self._send(payload)
    
    async def send_markdown(self, title: str, content: str) -> bool:
        """
        发送Markdown消息
        
        Args:
            title: 标题
            content: Markdown内容
            
        Returns:
            是否发送成功
        """
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": content
            }
        }
        
        return await self._send(payload)
    
    async def send_negative_alert(self, brand_name: str, news_title: str, 
                                   news_url: str, sentiment_score: float) -> bool:
        """
        发送负面舆情预警
        
        Args:
            brand_name: 品牌名称
            news_title: 新闻标题
            news_url: 新闻链接
            sentiment_score: 情感分数
            
        Returns:
            是否发送成功
        """
        title = f"🚨 负面舆情预警 - {brand_name}"
        
        content = f"""## 🚨 负面舆情预警

**品牌**: {brand_name}

**新闻标题**: {news_title}

**情感分数**: {sentiment_score:.2f} (分数越低越负面)

**链接**: [点击查看原文]({news_url})

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*此消息由大客户舆情监测系统自动发送*
"""
        
        return await self.send_markdown(title, content)
    
    async def send_daily_summary(self, date: str, top_news: List[Dict]) -> bool:
        """
        发送每日舆情摘要
        
        Args:
            date: 日期
            top_news: Top新闻列表
            
        Returns:
            是否发送成功
        """
        title = f"📊 每日舆情摘要 - {date}"
        
        news_list_md = ""
        for i, news in enumerate(top_news[:10], 1):
            sentiment_emoji = "🟢" if news.get("sentiment_label") == "positive" else "🔴" if news.get("sentiment_label") == "negative" else "🟡"
            news_list_md += f"{i}. {sentiment_emoji} [{news.get('brand_name')}]({news.get('url')}) - {news.get('title')[:30]}...\n"
        
        content = f"""## 📊 每日舆情摘要 ({date})

### Top 10 热门新闻

{news_list_md}

---
*此消息由大客户舆情监测系统自动发送*
"""
        
        return await self.send_markdown(title, content)
    
    async def _send(self, payload: Dict) -> bool:
        """
        发送请求到钉钉
        
        Args:
            payload: 请求体
            
        Returns:
            是否发送成功
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.webhook_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("errcode") == 0:
                        print("钉钉消息发送成功")
                        return True
                    else:
                        print(f"钉钉消息发送失败: {result}")
                        return False
                else:
                    print(f"钉钉请求失败: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"钉钉消息发送异常: {e}")
            return False


# 全局钉钉服务实例
dingtalk_service = DingTalkService()
