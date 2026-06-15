# 项目文件清单

## 根目录

- `.env.example` - 环境变量示例
- `.gitignore` - Git忽略文件
- `CHANGELOG.md` - 更新日志
- `CONTRIBUTING.md` - 贡献指南
- `docker-compose.yml` - Docker编排
- `LICENSE` - 许可证
- `README.md` - 项目说明
- `SECURITY.md` - 安全策略

## 后端 (backend/)

### 配置文件
- `requirements.txt` - Python依赖
- `Dockerfile` - Docker镜像

### 应用代码 (app/)
- `__init__.py` - 包初始化
- `main.py` - FastAPI入口
- `config.py` - 配置管理
- `models.py` - 数据库模型
- `schemas.py` - Pydantic模型
- `database.py` - 数据库连接

### 服务层 (services/)
- `__init__.py` - 包初始化
- `search.py` - 搜索服务
- `sentiment.py` - 情感分析
- `dingtalk.py` - 钉钉通知
- `scheduler.py` - 定时任务

### 路由层 (routers/)
- `__init__.py` - 包初始化
- `brands.py` - 品牌管理API
- `news.py` - 新闻搜索API
- `dashboard.py` - 展板数据API

## 前端 (frontend/)

### 配置文件
- `package.json` - Node依赖
- `tsconfig.json` - TypeScript配置
- `tsconfig.node.json` - Node配置
- `vite.config.ts` - Vite配置
- `index.html` - HTML模板

### 源代码 (src/)
- `main.tsx` - 入口文件
- `App.tsx` - 主组件
- `index.css` - 全局样式

### 页面 (pages/)
- `Dashboard.tsx` - 信息展板
- `Search.tsx` - 舆情搜索
- `Brands.tsx` - 品牌管理
- `Analytics.tsx` - 数据分析

### 服务 (services/)
- `api.ts` - API接口

## 脚本 (scripts/)
- `import_brands.py` - 品牌导入脚本

## 文档 (docs/)
- `USAGE.md` - 使用指南
- `TESTING.md` - 测试指南
- `FAQ.md` - 常见问题
- `ARCHITECTURE.md` - 架构文档
- `ALIYUN_DEPLOY.md` - 阿里云部署

## GitHub配置 (.github/)
- `workflows/deploy-frontend.yml` - 前端部署
- `workflows/deploy-backend.yml` - 后端部署
