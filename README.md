# A2E Protocol (AI-to-Everything)

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
  <a href="https://github.com/gulou69/AI-to-Everything/releases"><img src="https://img.shields.io/badge/version-1.0.0-green.svg" alt="Version"></a>
  <a href="https://github.com/gulou69/AI-to-Everything/issues"><img src="https://img.shields.io/github/issues/gulou69/AI-to-Everything.svg" alt="Issues"></a>
</p>

<p align="center">
  <a href="#english-documentation">English</a> | <a href="#中文文档">中文</a>
</p>

---

# English Documentation

## Introduction

**A2E (AI-to-Everything) Protocol** is an open-source protocol standard for AI service invocation, designed to bridge the gap between **AI Agents and real-world services**.

Traditional API documentation (e.g., Swagger/OpenAPI) is written for developers. The A2E protocol is an interface description standard designed specifically for **Large Language Models (LLMs)** -- enabling AI to **autonomously discover, understand, and invoke** real-world services.

### Why A2E?

| Dimension | Traditional API (OpenAPI/Swagger) | A2E Protocol |
|-----------|-----------------------------------|--------------|
| Target Audience | Developers | AI Agents |
| Description Style | Technical specification | Semantic description (natural language) |
| Integration | Requires coding | AI autonomous invocation |
| Service Discovery | Static documentation | Dynamic semantic search |
| Auth Model | Multiple standards | Unified platform token |

### Features

- **AI-Native** -- Interface description format designed for LLMs
- **Semantic Discovery** -- Natural language service search
- **Secure & Trusted** -- Built-in authentication and permission management
- **Transaction Support** -- Standardized payment and order workflow
- **Multi-language SDKs** -- Go / Python / JavaScript ready to use

## Quick Start

### Installation

**Go**
```bash
go get github.com/gulou69/AI-to-Everything/sdk/go
```

**Python**
```bash
pip install a2e-protocol
```

**JavaScript / TypeScript**
```bash
npm install a2e-protocol
```

### Usage Examples

<details>
<summary>Go</summary>

```go
package main

import (
    "fmt"
    a2e "github.com/gulou69/AI-to-Everything/sdk/go"
)

func main() {
    client := a2e.NewClient("https://api.a2e-platform.com")

    // Search services
    services, _ := client.SearchServices("milk tea shop")

    // Get protocol
    protocol, _ := client.GetProtocol(services[0].ID)

    // Execute service
    result, _ := client.Execute(protocol, map[string]interface{}{
        "action": "get_menu",
    })

    fmt.Println(result)
}
```
</details>

<details>
<summary>Python</summary>

```python
from a2e import A2EClient

client = A2EClient("https://api.a2e-platform.com")

# Search services
services = client.search_services("milk tea shop")

# Get protocol
protocol = client.get_protocol(services[0].id)

# Execute service
result = client.execute(protocol, {"action": "get_menu"})
print(result)
```
</details>

<details>
<summary>JavaScript / TypeScript</summary>

```typescript
import { A2EClient } from 'a2e-protocol';

const client = new A2EClient('https://api.a2e-platform.com');

// Search services
const services = await client.searchServices('milk tea shop');

// Get protocol
const protocol = await client.getProtocol(services[0].id);

// Execute service
const result = await client.execute(protocol, { action: 'get_menu' });
console.log(result);
```
</details>

## Protocol Specification

The A2E protocol uses YAML/JSON format to describe services, consisting of **8 core modules**:

| Module | Description |
|--------|-------------|
| `version` | Protocol version |
| `service` | Service metadata (id, name, type, provider) |
| `semantic` | Semantic description for LLM comprehension |
| `authentication` | Authentication methods |
| `permissions` | Permissions and pricing |
| `data_format` | Data structure definitions |
| `endpoints` | Callable endpoints |
| `error_handling` | Error codes and retry strategies |

### Protocol Example

```yaml
a2e_protocol:
  version: "1.0.0"

  service:
    id: "service_001"
    name: "Tea Shop"
    type: "food_delivery"

  semantic:
    description: "Offers various milk tea and fruit tea beverages with delivery support"
    keywords: ["milk tea", "beverages", "delivery"]
    capabilities:
      - "Online ordering"
      - "Custom flavors"
    ai_instruction: "You are an AI assistant for a tea shop, helping users browse the menu, place orders, and check order status"

  authentication:
    required: true
    methods:
      - type: "platform_token"

  endpoints:
    - name: "get_menu"
      description: "Get the shop menu"
      method: "POST"
      path: "/execute/get_menu"
```

Full specification: [A2E Protocol Specification](spec/a2e-protocol-spec.md)

## SDK

| SDK | Status | Docs |
|-----|--------|------|
| [Go SDK](sdk/go) | Available | [README](sdk/go/README.md) |
| [Python SDK](sdk/python) | Available | [README](sdk/python/README.md) |
| [JavaScript SDK](sdk/javascript) | Available | [README](sdk/javascript/README.md) |

## Examples

| Example | Description |
|---------|-------------|
| [AI Agent Integration](examples/ai-agent-demo) | Demonstrates how an AI Agent invokes A2E services |
| [Service Provider](examples/provider-demo) | Demonstrates how to build an A2E-compliant service |

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  AI Agent   │────>│ A2E Platform │────>│   Provider   │
│ (LLM-based) │<────│   (Gateway)  │<────│  (Services)  │
└─────────────┘     └──────────────┘     └──────────────┘
       │                   │                     │
       │    A2E Protocol   │    HTTP / REST      │
       └───────────────────┴─────────────────────┘
```

**Workflow:**

1. **Discover** -- AI Agent discovers available services on the platform via semantic search
2. **Understand** -- Retrieves the A2E protocol file; the LLM parses the semantic description to understand service capabilities
3. **Authenticate** -- Completes identity verification via platform token
4. **Execute** -- AI Agent constructs requests and invokes service endpoints
5. **Transact** -- For paid services, completes payment through the standardized order workflow

## Use Cases

| Scenario | Description |
|----------|-------------|
| Food Delivery | AI assistant orders milk tea and meals for users |
| Transportation | AI assistant books rides and tickets for users |
| Shopping | AI assistant compares prices and places orders for users |
| Home Services | AI assistant books cleaning and repair services for users |

## Contributing

We welcome all forms of contributions!

- [Report Bugs](https://github.com/gulou69/AI-to-Everything/issues)
- [Suggest Features](https://github.com/gulou69/AI-to-Everything/issues)
- Improve Documentation
- Submit Code

Please read the [Contributing Guide](CONTRIBUTING.md) for details.

## Roadmap

- [x] v1.0 -- Core protocol specification
- [ ] v1.1 -- Streaming response support
- [ ] v1.2 -- Multi-language protocol descriptions
- [ ] v2.0 -- Smart contract integration

---

# 中文文档

## 简介

**A2E (AI-to-Everything) Protocol** 是一个开源的AI服务调用协议标准，旨在建立 **AI Agent 与现实世界服务** 之间的桥梁。

传统的API文档（如 Swagger/OpenAPI）是为开发者编写的，而 A2E 协议是专门为 **大语言模型（LLM）** 设计的接口描述标准——让AI能够 **自主发现、理解并调用** 各种现实世界的服务。

### 为什么需要 A2E？

| 维度 | 传统API (OpenAPI/Swagger) | A2E协议 |
|------|--------------------------|---------|
| 目标用户 | 开发者 | AI Agent |
| 描述方式 | 技术性描述 | 语义化描述（自然语言） |
| 集成方式 | 需要编程集成 | AI自主调用 |
| 服务发现 | 静态文档 | 动态语义搜索 |
| 认证模型 | 多种标准 | 统一平台令牌 |

### 特性

- **AI-Native** — 专为LLM设计的接口描述格式
- **语义发现** — 支持自然语言搜索服务
- **安全可信** — 内置身份认证与权限管理
- **交易支持** — 标准化的支付与订单流程
- **多语言SDK** — Go / Python / JavaScript 开箱即用

## 快速开始

### 安装

**Go**
```bash
go get github.com/gulou69/AI-to-Everything/sdk/go
```

**Python**
```bash
pip install a2e-protocol
```

**JavaScript / TypeScript**
```bash
npm install a2e-protocol
```

### 使用示例

<details>
<summary>Go</summary>

```go
package main

import (
    "fmt"
    a2e "github.com/gulou69/AI-to-Everything/sdk/go"
)

func main() {
    client := a2e.NewClient("https://api.a2e-platform.com")

    // 搜索服务
    services, _ := client.SearchServices("奶茶店")

    // 获取协议
    protocol, _ := client.GetProtocol(services[0].ID)

    // 执行服务
    result, _ := client.Execute(protocol, map[string]interface{}{
        "action": "get_menu",
    })

    fmt.Println(result)
}
```
</details>

<details>
<summary>Python</summary>

```python
from a2e import A2EClient

client = A2EClient("https://api.a2e-platform.com")

# 搜索服务
services = client.search_services("奶茶店")

# 获取协议
protocol = client.get_protocol(services[0].id)

# 执行服务
result = client.execute(protocol, {"action": "get_menu"})
print(result)
```
</details>

<details>
<summary>JavaScript / TypeScript</summary>

```typescript
import { A2EClient } from 'a2e-protocol';

const client = new A2EClient('https://api.a2e-platform.com');

// 搜索服务
const services = await client.searchServices('奶茶店');

// 获取协议
const protocol = await client.getProtocol(services[0].id);

// 执行服务
const result = await client.execute(protocol, { action: 'get_menu' });
console.log(result);
```
</details>

## 协议规范

A2E协议采用 YAML/JSON 格式描述服务，包含 **8大核心模块**：

| 模块 | 说明 |
|------|------|
| `version` | 协议版本 |
| `service` | 服务基本信息（id、名称、类型、提供商） |
| `semantic` | 语义描述，供LLM理解服务能力 |
| `authentication` | 认证方式 |
| `permissions` | 权限与费用说明 |
| `data_format` | 数据结构定义 |
| `endpoints` | 可调用端点 |
| `error_handling` | 错误码与处理策略 |

### 协议示例

```yaml
a2e_protocol:
  version: "1.0.0"

  service:
    id: "service_001"
    name: "某某奶茶店"
    type: "food_delivery"

  semantic:
    description: "提供各类奶茶、果茶饮品，支持外卖配送"
    keywords: ["奶茶", "饮品", "外卖"]
    capabilities:
      - "在线点餐"
      - "自定义口味"
    ai_instruction: "你是一个奶茶店的AI助手，可以帮助用户浏览菜单、下单和查询订单状态"

  authentication:
    required: true
    methods:
      - type: "platform_token"

  endpoints:
    - name: "get_menu"
      description: "获取店铺菜单"
      method: "POST"
      path: "/execute/get_menu"
```

完整规范请参阅 [A2E Protocol Specification](spec/a2e-protocol-spec.md)

## SDK

| SDK | 状态 | 文档 |
|-----|------|------|
| [Go SDK](sdk/go) | 可用 | [README](sdk/go/README.md) |
| [Python SDK](sdk/python) | 可用 | [README](sdk/python/README.md) |
| [JavaScript SDK](sdk/javascript) | 可用 | [README](sdk/javascript/README.md) |

## 示例

| 示例 | 说明 |
|------|------|
| [AI Agent 接入示例](examples/ai-agent-demo) | 展示如何让 AI Agent 调用 A2E 服务 |
| [服务提供商示例](examples/provider-demo) | 展示如何创建符合 A2E 协议的服务 |

## 架构

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  AI Agent   │────>│ A2E Platform │────>│   Provider   │
│  (LLM驱动)  │<────│   (网关)      │<────│   (服务商)    │
└─────────────┘     └──────────────┘     └──────────────┘
       │                   │                     │
       │    A2E Protocol   │    HTTP / REST      │
       └───────────────────┴─────────────────────┘
```

**工作流程：**

1. **发现** — AI Agent 通过语义搜索在平台发现可用服务
2. **理解** — 获取 A2E 协议文件，LLM 解析语义描述理解服务能力
3. **认证** — 通过平台令牌完成身份验证
4. **执行** — AI Agent 构建请求并调用服务端点
5. **交易** — 涉及付费服务时，通过标准化订单流程完成支付

## 应用场景

| 场景 | 描述 |
|------|------|
| 餐饮外卖 | AI助手帮用户点奶茶、订餐，自动完成下单和支付 |
| 出行服务 | AI助手帮用户打车、订票，实时跟踪行程 |
| 购物消费 | AI助手帮用户比价、下单、跟踪物流 |
| 生活服务 | AI助手帮用户预约家政、维修等服务 |

## 贡献

我们欢迎所有形式的贡献！

- [报告Bug](https://github.com/gulou69/AI-to-Everything/issues)
- [提出建议](https://github.com/gulou69/AI-to-Everything/issues)
- 改进文档
- 提交代码

请阅读 [贡献指南](CONTRIBUTING.md) 了解详情。

## 路线图

- [x] v1.0 — 基础协议规范
- [ ] v1.1 — 流式响应支持
- [ ] v1.2 — 多语言协议描述
- [ ] v2.0 — 智能合约集成

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
