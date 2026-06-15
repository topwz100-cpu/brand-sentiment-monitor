# 大客户舆情监测系统

## 项目简介

大客户舆情监测系统，实时监测全网品牌资讯动态，支持搜索、展板展示、情感分析和钉钉预警。

## 功能特性

- ✅ **品牌搜索**：输入品牌名称搜索全网最新资讯
- ✅ **Top20展板**：每日自动更新热门新闻
- ✅ **情感分析**：自动判断新闻情感倾向
- ✅ **舆情预警**：负面新闻自动钉钉通知
- ✅ **数据看板**：品牌分布、情感趋势可视化
- ✅ **品牌管理**：灵活管理监测品牌列表

## 技术栈

- **前端**：React 18 + TypeScript + Ant Design + ECharts
- **后端**：Python 3.11 + FastAPI + SQLAlchemy
- **数据库**：PostgreSQL + Redis
- **搜索**：Tavily API + 微博搜索
- **部署**：Docker + GitHub Pages + 阿里云

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd brand-sentiment-monitor
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/sentiment_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Tavily API密钥
TAVILY_API_KEY=your_tavily_api_key

# 钉钉机器人Webhook
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=your_token
```

### 3. Docker部署

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
```

### 4. 本地开发

**后端：**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

## API文档

启动后访问：http://localhost:8000/docs

## 部署指南

### GitHub Pages部署前端

1. 在GitHub创建仓库
2. 推送代码
3. 配置GitHub Actions自动部署

### 阿里云部署后端

1. 购买阿里云ECS实例
2. 安装Docker和Docker Compose
3. 配置安全组开放8000端口
4. 部署后端服务

## 项目结构

```
brand-sentiment-monitor/
├── backend/          # 后端服务
├── frontend/         # 前端应用
├── data/             # 数据文件
├── docker-compose.yml
└── README.md
```

## 注意事项

- 首次启动需要配置Tavily API密钥
- 钉钉机器人需要配置安全设置（IP白名单或加签）
- 微博搜索需要配置Cookie（可选）

## 许可证

MIT
