# AI Agent Integration Demo

This example demonstrates how an external AI Agent (e.g., ChatGPT, Claude) can discover and invoke services through the A2E protocol.

本示例展示外部 AI Agent（如 ChatGPT、Claude）如何通过 A2E 协议发现和调用服务。

## Directory Structure / 目录结构

```
ai-agent-demo/
├── README.md
└── python/
    ├── main.py           # AI Agent demo script
    └── requirements.txt  # Dependencies
```

## How It Works / 工作原理

```
User → AI Agent → A2E Platform → Service Provider
用户  →  AI助手  →  A2E平台    →  服务提供商
```

### Flow / 流程

1. **Service Discovery / 服务发现**: AI Agent searches for services using natural language keywords
2. **Get Protocol / 获取协议**: AI Agent retrieves the A2E protocol document to understand the service
3. **Authentication / 身份认证**: AI Agent obtains a Consumer Token on behalf of the user
4. **Execute / 执行服务**: AI Agent calls service endpoints as described in the protocol
5. **Handle Results / 处理结果**: AI Agent interprets results and presents them to the user

## Run / 运行

```bash
cd python
pip install -r requirements.txt
python main.py
```

## Configuration / 配置

Set the A2E platform URL via environment variable:

```bash
export A2E_BASE_URL=https://api.a2e-platform.com
# or
set A2E_BASE_URL=https://api.a2e-platform.com
```
