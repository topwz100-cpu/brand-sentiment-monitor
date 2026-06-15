# 贡献指南

感谢您对项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 1. 提交Issue

如果您发现了bug或有新功能建议，请提交Issue：

1. 点击仓库的"Issues"标签
2. 点击"New issue"按钮
3. 选择Issue类型（Bug报告/功能建议）
4. 填写详细信息
5. 提交Issue

### 2. 提交Pull Request

如果您想直接贡献代码，请按照以下步骤：

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

### 3. 代码规范

#### Python代码规范

- 使用PEP 8风格
- 函数和变量使用snake_case
- 类名使用PascalCase
- 添加docstring注释

```python
def example_function(param1: str, param2: int) -> bool:
    """
    示例函数
    
    Args:
        param1: 参数1
        param2: 参数2
        
    Returns:
        返回结果
    """
    return True
```

#### TypeScript代码规范

- 使用ESLint配置
- 函数和变量使用camelCase
- 接口名使用PascalCase
- 添加JSDoc注释

```typescript
interface UserProps {
  name: string;
  age: number;
}

function exampleFunction(user: UserProps): boolean {
  return user.age > 18;
}
```

### 4. 提交规范

提交信息格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(search): 添加微博搜索功能

- 实现微博网页抓取
- 添加数据解析和格式化
- 更新API文档

Closes #123
```

### 5. 测试要求

提交代码前请确保：

- [ ] 所有测试通过
- [ ] 代码覆盖率不降低
- [ ] 手动测试通过
- [ ] 文档已更新

### 6. 文档更新

如果修改了API或功能，请更新相关文档：

- README.md
- API文档
- 使用指南
- 常见问题

## 开发环境

### 本地开发

```bash
# 克隆仓库
git clone <repo-url>
cd brand-sentiment-monitor

# 安装依赖
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 启动服务
cd ../backend && uvicorn app.main:app --reload
cd ../frontend && npm run dev
```

### Docker开发

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 联系方式

如有任何问题，请联系：

- Email: your-email@example.com
- GitHub Issues: [项目Issues页面]

## 许可证

本项目采用 MIT 许可证。
