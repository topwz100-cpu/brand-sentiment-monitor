# 安全策略

## 报告安全漏洞

如果您发现了安全漏洞，请不要在公共Issue中报告。请按照以下方式报告：

1. 发送邮件至：security@your-domain.com
2. 邮件主题：[SECURITY] 漏洞描述
3. 邮件内容：
   - 漏洞描述
   - 复现步骤
   - 影响范围
   - 建议修复方案

## 安全更新

我们会定期发布安全更新，请关注：

- GitHub Security Advisories
- 项目Release页面
- 邮件通知

## 安全最佳实践

### 1. 环境变量保护

- 不要将 `.env` 文件提交到版本控制
- 使用强密码
- 定期更换API密钥

### 2. 数据库安全

- 使用强密码
- 限制数据库访问IP
- 定期备份数据
- 启用SSL连接

### 3. API安全

- 使用HTTPS
- 限制请求频率
- 验证输入数据
- 使用CORS保护

### 4. 容器安全

- 使用官方镜像
- 定期更新基础镜像
- 限制容器权限
- 扫描镜像漏洞

## 依赖安全

### 检查依赖漏洞

```bash
# Python依赖
pip install safety
safety check

# Node.js依赖
npm audit
npm audit fix
```

### 更新依赖

```bash
# Python依赖
pip list --outdated
pip install --upgrade <package>

# Node.js依赖
npm outdated
npm update
```

## 安全工具

### 静态代码分析

```bash
# Python
pip install bandit
bandit -r .

# JavaScript
npm install --save-dev eslint-plugin-security
npx eslint . --ext .js,.jsx,.ts,.tsx
```

### 容器扫描

```bash
# 使用Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image brand-sentiment-monitor_backend
```

## 安全联系人

- 安全团队：security@your-domain.com
- 项目负责人：your-email@example.com
