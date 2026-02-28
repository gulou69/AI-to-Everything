# 贡献指南

感谢您对 A2E Protocol 的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告问题

如果您发现了 Bug 或有功能建议，请通过 [GitHub Issues](https://github.com/gulou69/AI-to-Everything/issues) 提交。

提交 Issue 时请包含：
- 清晰的标题和描述
- 复现步骤（如果是 Bug）
- 期望行为和实际行为
- 相关的代码片段或截图

### 提交代码

1. **Fork 仓库**
   ```bash
   git clone https://github.com/gulou69/AI-to-Everything.git
   cd AI-to-Everything
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **进行修改**
   - 遵循项目的代码风格
   - 添加必要的测试
   - 更新相关文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add some feature"
   ```

5. **推送并创建 PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit 规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

| 类型 | 描述 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式调整 |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具调整 |

示例：
```
feat: add Python SDK support
fix: resolve authentication issue
docs: update API reference
```

## 代码规范

### Go 代码
- 使用 `gofmt` 格式化
- 遵循 [Effective Go](https://go.dev/doc/effective_go)
- 导出函数必须有注释

### Python 代码
- 遵循 PEP 8
- 使用 Type Hints
- 使用 Black 格式化

### JavaScript 代码
- 使用 ESLint + Prettier
- 使用 TypeScript

## 开发环境

### 要求
- Go 1.21+
- Python 3.10+
- Node.js 18+

### 设置
```bash
# 安装依赖
make setup

# 运行测试
make test

# 检查代码
make lint
```

## 文档贡献

文档位于 `docs/` 目录，使用 Markdown 格式。

修改文档后请本地预览确认无误。

## 行为准则

请尊重所有参与者，保持友善和专业的交流氛围。

## 联系方式

如有问题，可通过以下方式联系：
- GitHub Issues
- Email: wcz2935772532@gmail.com

再次感谢您的贡献！
