# 阿里云服务器部署指南

## 服务器要求

- Ubuntu 20.04+ / CentOS 7+
- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 内存
- 开放端口: 80, 443, 8000

## 部署步骤

### 1. 安装Docker和Docker Compose

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 配置环境变量

```bash
# 创建项目目录
mkdir -p /opt/brand-sentiment-monitor
cd /opt/brand-sentiment-monitor

# 创建环境变量文件
cat > .env << EOF
DATABASE_URL=postgresql://sentiment_user:your_password@localhost:5432/sentiment_db
REDIS_URL=redis://localhost:6379/0
TAVILY_API_KEY=your_tavily_api_key
DINGTALK_WEBHOOK=your_dingtalk_webhook
EOF
```

### 3. 部署服务

```bash
# 拉取代码
git clone <your-repo-url> .

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
```

### 4. 配置Nginx反向代理

```bash
# 安装Nginx
sudo apt install nginx -y

# 创建配置文件
sudo cat > /etc/nginx/sites-available/brand-sentiment << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 启用配置
sudo ln -s /etc/nginx/sites-available/brand-sentiment /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. 配置SSL证书

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 申请证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### 6. 配置防火墙

```bash
# 开放端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw enable
```

## 维护命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend

# 重启服务
docker-compose restart

# 更新代码
git pull
docker-compose up -d --build

# 备份数据库
docker exec brand-sentiment-monitor_db_1 pg_dump -U sentiment_user sentiment_db > backup.sql

# 恢复数据库
docker exec -i brand-sentiment-monitor_db_1 psql -U sentiment_user sentiment_db < backup.sql
```

## 监控

```bash
# 查看容器资源使用
docker stats

# 查看系统日志
sudo journalctl -u docker.service -f
```
