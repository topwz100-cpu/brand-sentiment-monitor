"""
搜索服务 - 整合多个新闻源
"""
import httpx
import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from ..config import settings


class SearchService:
    """搜索服务"""
    
    def __init__(self):
        self.tavily_api_key = settings.TAVILY_API_KEY
        self.tavily_base_url = "https://api.tavily.com"
        
    async def search_news(self, query: str, days: int = 7, max_results: int = 20) -> List[Dict]:
        """
        搜索新闻 - 使用聚合新闻API
        
        Args:
            query: 搜索关键词
            days: 搜索最近几天的数据
            max_results: 最大结果数
            
        Returns:
            新闻列表
        """
        # 使用聚合新闻API（免费、快速）
        results = await self._search_news_api(query, max_results)
        
        # 如果聚合API失败，回退到Tavily
        if not results:
            results = await self._search_tavily(query, max_results)
        
        return results
    
    async def _search_news_api(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        使用聚合新闻API搜索
        
        免费API来源：
        - 新浪新闻RSS
        - 腾讯新闻
        - 网易新闻
        - 搜狐新闻
        """
        news_list = []
        
        # 并行搜索多个新闻源
        tasks = [
            self._search_sina_news(query, max_results // 4),
            self._search_tencent_news(query, max_results // 4),
            self._search_netease_news(query, max_results // 4),
            self._search_sohu_news(query, max_results // 4),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                news_list.extend(result)
        
        # 去重（基于URL）
        seen_urls = set()
        unique_news = []
        for item in news_list:
            url = item.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_news.append(item)
        
        # 按时间排序
        unique_news.sort(key=lambda x: x.get("published_at", datetime.min), reverse=True)
        
        return unique_news[:max_results]
    
    async def _search_sina_news(self, query: str, max_results: int = 5) -> List[Dict]:
        """搜索新浪新闻"""
        try:
            url = f"https://search.sina.com.cn/?q={query}&c=news&from=channel&ie=utf-8"
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                response = await client.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    # 解析搜索结果
                    soup = BeautifulSoup(response.text, 'html.parser')
                    news_list = []
                    
                    # 新浪搜索结果解析
                    for item in soup.find_all('div', class_='box-result')[:max_results]:
                        try:
                            title_tag = item.find('h2')
                            if title_tag:
                                title = title_tag.get_text(strip=True)
                                link = title_tag.find('a', href=True)
                                url = link['href'] if link else ""
                                
                                news_item = {
                                    "title": title,
                                    "content": "",
                                    "url": url,
                                    "source": "新浪新闻",
                                    "published_at": datetime.now(),
                                    "source_type": "news"
                                }
                                news_list.append(news_item)
                        except Exception:
                            continue
                    
                    return news_list
                    
        except Exception as e:
            print(f"新浪新闻搜索失败: {e}")
            
        return []
    
    async def _search_tencent_news(self, query: str, max_results: int = 5) -> List[Dict]:
        """搜索腾讯新闻"""
        try:
            # 腾讯新闻搜索API
            url = f"https://www.qq.com/search.htm?pg=search&st=news&w={query}"
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                response = await client.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    news_list = []
                    
                    # 解析搜索结果
                    for item in soup.find_all('div', class_='result')[:max_results]:
                        try:
                            title_tag = item.find('h3')
                            if title_tag:
                                title = title_tag.get_text(strip=True)
                                link = title_tag.find('a', href=True)
                                url = link['href'] if link else ""
                                
                                news_item = {
                                    "title": title,
                                    "content": "",
                                    "url": url,
                                    "source": "腾讯新闻",
                                    "published_at": datetime.now(),
                                    "source_type": "news"
                                }
                                news_list.append(news_item)
                        except Exception:
                            continue
                    
                    return news_list
                    
        except Exception as e:
            print(f"腾讯新闻搜索失败: {e}")
            
        return []
    
    async def _search_netease_news(self, query: str, max_results: int = 5) -> List[Dict]:
        """搜索网易新闻"""
        try:
            # 网易新闻搜索
            url = f"https://www.163.com/search?keyword={query}"
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                response = await client.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    news_list = []
                    
                    # 解析搜索结果
                    for item in soup.find_all('div', class_='item')[:max_results]:
                        try:
                            title_tag = item.find('h3')
                            if title_tag:
                                title = title_tag.get_text(strip=True)
                                link = title_tag.find('a', href=True)
                                url = link['href'] if link else ""
                                
                                news_item = {
                                    "title": title,
                                    "content": "",
                                    "url": url,
                                    "source": "网易新闻",
                                    "published_at": datetime.now(),
                                    "source_type": "news"
                                }
                                news_list.append(news_item)
                        except Exception:
                            continue
                    
                    return news_list
                    
        except Exception as e:
            print(f"网易新闻搜索失败: {e}")
            
        return []
    
    async def _search_sohu_news(self, query: str, max_results: int = 5) -> List[Dict]:
        """搜索搜狐新闻"""
        try:
            # 搜狐新闻搜索
            url = f"https://search.sohu.com/?keyword={query}"
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                response = await client.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    news_list = []
                    
                    # 解析搜索结果
                    for item in soup.find_all('div', class_='result')[:max_results]:
                        try:
                            title_tag = item.find('h4')
                            if title_tag:
                                title = title_tag.get_text(strip=True)
                                link = title_tag.find('a', href=True)
                                url = link['href'] if link else ""
                                
                                news_item = {
                                    "title": title,
                                    "content": "",
                                    "url": url,
                                    "source": "搜狐新闻",
                                    "published_at": datetime.now(),
                                    "source_type": "news"
                                }
                                news_list.append(news_item)
                        except Exception:
                            continue
                    
                    return news_list
                    
        except Exception as e:
            print(f"搜狐新闻搜索失败: {e}")
            
        return []
    
    async def _search_tavily(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        使用Tavily API搜索（备用方案）
        """
        try:
            url = f"{self.tavily_base_url}/search"
            
            payload = {
                "api_key": self.tavily_api_key,
                "query": query,
                "search_depth": "basic",  # 使用basic模式，更快
                "include_answer": False,
                "include_images": False,
                "include_raw_content": False,
                "max_results": max_results,
                "include_domains": [],
                "exclude_domains": []
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                results = data.get("results", [])
                
                news_list = []
                for item in results:
                    news_item = {
                        "title": item.get("title", ""),
                        "content": item.get("content", ""),
                        "url": item.get("url", ""),
                        "source": item.get("source", ""),
                        "published_at": self._parse_date(item.get("published_date", "")),
                        "source_type": "news"
                    }
                    news_list.append(news_item)
                
                return news_list
                
        except Exception as e:
            print(f"Tavily搜索失败: {e}")
            return []
    
    async def search_weibo(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        搜索微博（通过网页抓取）
        """
        # 微博搜索需要登录，暂时返回空
        return []
    
    async def search_brand(self, brand_name: str, days: int = 7) -> List[Dict]:
        """
        搜索品牌相关资讯（新闻+微博）
        """
        # 搜索新闻
        news_results = await self.search_news(brand_name, days, settings.SEARCH_MAX_RESULTS)
        
        # 按时间排序（处理None值，优先展示近期新闻）
        def sort_key(x):
            dt = x.get("published_at")
            if dt is None:
                return datetime.min
            return dt
        
        news_results.sort(key=sort_key, reverse=True)
        
        return news_results
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """解析日期字符串"""
        if not date_str:
            return None
            
        formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%a, %d %b %Y %H:%M:%S %Z"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
                
        return None


# 全局搜索服务实例
search_service = SearchService()
