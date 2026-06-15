# 前端部署到GitHub Pages配置
# 需要在GitHub仓库Settings > Pages中设置Source为GitHub Actions

# 1. 创建GitHub仓库并推送代码
# 2. 在仓库Settings > Secrets and variables > Actions中添加以下secrets:
#    - VITE_API_URL: 你的后端API地址 (例如: https://api.yourdomain.com)

# 3. 在仓库Settings > Pages中:
#    - Source: GitHub Actions
#    - Branch: gh-pages

# 4. 推送代码后自动部署
