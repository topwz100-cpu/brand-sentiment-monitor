# 测试指南

## 单元测试

### 后端测试

```bash
cd backend

# 安装测试依赖
pip install pytest pytest-asyncio httpx

# 运行测试
pytest

# 运行特定测试
pytest tests/test_search.py

# 生成测试报告
pytest --cov=app --cov-report=html
```

### 前端测试

```bash
cd frontend

# 安装测试依赖
npm install --save-dev @testing-library/react @testing-library/jest-dom

# 运行测试
npm test

# 生成测试报告
npm test -- --coverage
```

## 集成测试

### API测试

```bash
# 测试搜索API
curl "http://localhost:8000/news/search?keyword=修丽可&days=7"

# 测试品牌API
curl "http://localhost:8000/brands/"

# 测试展板API
curl "http://localhost:8000/dashboard/top20"
```

### 端到端测试

```bash
# 安装Playwright
npm install --save-dev @playwright/test
npx playwright install

# 运行测试
npx playwright test

# 查看测试报告
npx playwright show-report
```

## 性能测试

### 负载测试

```bash
# 安装Locust
pip install locust

# 创建测试文件
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def search_news(self):
        self.client.get("/news/search?keyword=修丽可&days=7")
    
    @task
    def get_dashboard(self):
        self.client.get("/dashboard/top20")
    
    @task
    def get_brands(self):
        self.client.get("/brands/")
EOF

# 运行测试
locust -f locustfile.py --host=http://localhost:8000
```

## 测试数据

### 测试品牌列表

```json
[
  "修丽可",
  "GNC健安喜",
  "兰蔻",
  "王小卤",
  "Swisse斯维诗"
]
```

### 测试搜索关键词

```json
[
  "修丽可 新品",
  "兰蔻 活动",
  "王小卤 营销",
  "Swisse 口碑",
  "GNC 质量"
]
```

## 测试检查清单

### 功能测试

- [ ] 品牌搜索功能正常
- [ ] Top20展板显示正确
- [ ] 情感分析结果准确
- [ ] 钉钉通知发送成功
- [ ] 定时任务执行正常
- [ ] 品牌管理功能完整

### 性能测试

- [ ] 搜索响应时间 < 3秒
- [ ] 展板加载时间 < 2秒
- [ ] 并发用户 > 100
- [ ] 数据库查询优化

### 安全测试

- [ ] API接口安全
- [ ] 数据库连接安全
- [ ] 环境变量保护
- [ ] 日志信息脱敏

## 测试报告

测试完成后，生成测试报告：

```bash
# 后端测试报告
pytest --html=report.html --self-contained-html

# 前端测试报告
npm test -- --coverage --watchAll=false

# 性能测试报告
locust -f locustfile.py --host=http://localhost:8000 --html=locust_report.html
```
