# 常见问题解答

## 部署问题

### Q: Docker启动失败？

**A:** 检查以下几点：
1. Docker和Docker Compose版本是否满足要求
2. 端口是否被占用（8000, 3000, 5432, 6379）
3. 环境变量是否正确配置
4. 查看日志：`docker-compose logs`

### Q: 前端无法访问后端API？

**A:** 
1. 检查后端服务是否正常运行
2. 检查CORS配置是否正确
3. 检查前端API地址配置
4. 查看浏览器控制台错误信息

### Q: 数据库连接失败？

**A:**
1. 检查数据库服务是否启动
2. 检查数据库连接字符串是否正确
3. 检查数据库用户权限
4. 查看数据库日志：`docker-compose logs db`

## 功能问题

### Q: 搜索不到结果？

**A:**
1. 检查Tavily API密钥是否有效
2. 检查网络连接是否正常
3. 尝试更换搜索关键词
4. 查看后端日志：`docker-compose logs backend`

### Q: 情感分析不准确？

**A:**
1. SnowNLP对短文本分析可能不够准确
2. 可以尝试使用更专业的NLP服务
3. 可以添加自定义词典提高准确性

### Q: 钉钉通知收不到？

**A:**
1. 检查Webhook地址是否正确
2. 检查钉钉机器人是否被禁言
3. 检查安全设置（IP白名单或加签）
4. 查看后端日志确认发送状态

### Q: 定时任务不执行？

**A:**
1. 检查定时任务配置是否正确
2. 检查系统时间是否正确
3. 手动触发测试：`docker exec brand-sentiment-monitor_backend_1 python -c "from app.services.scheduler import scheduler_service; scheduler_service.daily_update()"`

## 性能问题

### Q: 搜索速度慢？

**A:**
1. 增加缓存机制
2. 优化数据库查询
3. 使用异步处理
4. 考虑使用CDN加速

### Q: 内存占用高？

**A:**
1. 优化数据库连接池
2. 清理过期缓存
3. 限制并发请求数
4. 监控内存使用情况

## 数据问题

### Q: 如何备份数据？

**A:**
```bash
# 备份数据库
docker exec brand-sentiment-monitor_db_1 pg_dump -U sentiment_user sentiment_db > backup.sql

# 备份Redis
docker exec brand-sentiment-monitor_redis_1 redis-cli BGSAVE
```

### Q: 如何恢复数据？

**A:**
```bash
# 恢复数据库
docker exec -i brand-sentiment-monitor_db_1 psql -U sentiment_user sentiment_db < backup.sql
```

### Q: 如何清空测试数据？

**A:**
```bash
# 清空数据库
docker exec brand-sentiment-monitor_db_1 psql -U sentiment_user sentiment_db -c "TRUNCATE TABLE news_articles, daily_top_news CASCADE;"
```

## 开发问题

### Q: 如何添加新的数据源？

**A:**
1. 在 `app/services/search.py` 中添加新的搜索方法
2. 实现数据解析和格式化
3. 在路由中调用新方法

### Q: 如何修改情感分析算法？

**A:**
1. 修改 `app/services/sentiment.py`
2. 可以替换为其他NLP库或服务
3. 更新测试用例

### Q: 如何添加新的通知方式？

**A:**
1. 在 `app/services/` 目录下创建新的通知服务
2. 实现发送方法
3. 在配置中添加相关配置
4. 在定时任务中调用

## 其他问题

### Q: 如何查看日志？

**A:**
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f db
docker-compose logs -f redis
```

### Q: 如何更新代码？

**A:**
```bash
# 拉取最新代码
git pull

# 重启服务
docker-compose up -d --build

# 清理旧镜像
docker image prune -f
```

### Q: 如何停止服务？

**A:**
```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

## 联系支持

如果以上问题无法解决，请联系技术支持团队。
