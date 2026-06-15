# 项目使用指南

## 快速开始

### 1. 环境准备

确保已安装：
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+ (本地开发)
- Node.js 18+ (本地开发)

### 2. 启动服务

```bash
# 克隆项目
git clone <your-repo-url>
cd brand-sentiment-monitor

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写必要的配置

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 3. 导入品牌数据

```bash
# 进入后端容器
docker exec -it brand-sentiment-monitor_backend_1 bash

# 运行导入脚本
python scripts/import_brands.py

# 或者手动导入
python -c "from scripts.import_brands import import_brands_from_excel; import_brands_from_excel('/app/data/brands.xlsx')"
```

### 4. 访问系统

- **前端页面**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 功能使用

### 信息展板

1. 打开 http://localhost:3000
2. 查看今日Top20热门新闻
3. 查看统计数据卡片

### 舆情搜索

1. 点击左侧菜单"舆情搜索"
2. 输入品牌名称或关键词
3. 选择时间范围
4. 点击搜索按钮

### 品牌管理

1. 点击左侧菜单"品牌管理"
2. 点击"添加品牌"按钮
3. 填写品牌信息
4. 保存

### 数据分析

1. 点击左侧菜单"数据分析"
2. 查看情感趋势图
3. 查看品牌分布图

## API使用示例

### 搜索新闻

```bash
curl "http://localhost:8000/news/search?keyword=修丽可&days=7&limit=20"
```

### 获取Top20

```bash
curl "http://localhost:8000/dashboard/top20"
```

### 获取统计数据

```bash
curl "http://localhost:8000/dashboard/stats"
```

## 定时任务

系统每天凌晨6点自动执行：
1. 搜索所有品牌的最新资讯
2. 进行情感分析
3. 计算热度分数
4. 生成Top20
5. 发送钉钉通知

## 常见问题

### Q: 如何修改定时任务时间？
A: 修改 `.env` 文件中的 `DAILY_UPDATE_HOUR` 和 `DAILY_UPDATE_MINUTE`

### Q: 如何添加更多品牌？
A: 在"品牌管理"页面点击"添加品牌"，或批量导入Excel文件

### Q: 钉钉通知不工作？
A: 检查 `DINGTALK_WEBHOOK` 配置是否正确，确保钉钉机器人已启用

### Q: 搜索不到结果？
A: 检查 `TAVILY_API_KEY` 是否有效，或尝试更换搜索关键词

## 技术支持

如有问题，请联系技术支持团队。
