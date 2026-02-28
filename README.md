# A2E Protocol (AI-to-Everything)

<p align="center">
  <strong>🤖 让AI从"处理信息"进化到"处理事务" | Evolving AI from "processing information" to "handling real-world tasks"</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
  <a href="https://github.com/gulou69/AI-to-Everything/releases"><img src="https://img.shields.io/badge/version-1.0.0-green.svg" alt="Version"></a>
  <a href="https://github.com/gulou69/AI-to-Everything/issues"><img src="https://img.shields.io/github/issues/gulou69/AI-to-Everything.svg" alt="Issues"></a>
</p>

<p align="center">
  <a href="#-简介">简介</a> •
  <a href="#-introduction">Introduction</a> •
  <a href="#-快速开始--quick-start">快速开始</a> •
  <a href="#-协议规范--protocol-spec">协议规范</a> •
  <a href="#sdk">SDK</a> •
  <a href="#-示例--examples">示例</a> •
  <a href="#-贡献--contributing">贡献</a>
</p>

---

## 📖 简介

**A2E (AI-to-Everything) Protocol** 是一个开源的AI服务调用协议标准，旨在建立**AI Agent与现实世界服务**之间的桥梁。

传统的API文档（如Swagger/OpenAPI）是为开发者编写的，而A2E协议是专门为**大语言模型（LLM）**设计的接口描述标准——让AI能够**自主发现、理解并调用**各种现实世界的服务。

### 为什么需要A2E？

| 维度 | 传统API (OpenAPI/Swagger) | A2E协议 |
|------|--------------------------|---------|
| 目标用户 | 开发者 | AI Agent |
| 描述方式 | 技术性描述 | 语义化描述（自然语言） |
| 集成方式 | 需要编程集成 | AI自主调用 |
| 服务发现 | 静态文档 | 动态语义搜索 |
| 认证模型 | 多种标准 | 统一平台令牌 |

---

## 📖 Introduction

**A2E (AI-to-Everything) Protocol** is an open-source protocol standard for AI service invocation, designed to bridge the gap between **AI Agents and real-world services**.

Traditional API documentation (e.g., Swagger/OpenAPI) is written for developers. The A2E protocol is an interface description standard designed specifically for **Large Language Models (LLMs)** — enabling AI to **autonomously discover, understand, and invoke** real-world services.

### Why A2E?

| Dimension | Traditional API (OpenAPI/Swagger) | A2E Protocol |
|-----------|-----------------------------------|--------------|
| Target Audience | Developers | AI Agents |
| Description Style | Technical specification | Semantic description (natural language) |
| Integration | Requires coding | AI autonomous invocation |
| Service Discovery | Static documentation | Dynamic semantic search |
| Auth Model | Multiple standards | Unified platform token |

---

## ✨ 特性 | Features

- 🤖 **AI-Native** — 专为LLM设计的接口描述格式 | Interface description format designed for LLMs
- 🔍 **语义发现 Semantic Discovery** — 支持自然语言搜索服务 | Natural language service search
- 🔐 **安全可信 Secure & Trusted** — 内置身份认证与权限管理 | Built-in authentication & permission management
- 💰 **交易支持 Transaction Support** — 标准化的支付与订单流程 | Standardized payment & order workflow
- 🔌 **多语言SDK Multi-language SDKs** — Go / Python / JavaScript 开箱即用 | Ready-to-use SDKs

---

## 🚀 快速开始 | Quick Start

### 安装 | Installation

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

### 使用示例 | Usage Examples

<details>
<summary>🟢 Go</summary>

```go
package main

import (
    "fmt"
    a2e "github.com/gulou69/AI-to-Everything/sdk/go"
)

func main() {
    client := a2e.NewClient("https://api.a2e-platform.com")

    // 搜索服务 | Search services
    services, _ := client.SearchServices("奶茶店")

    // 获取协议 | Get protocol
    protocol, _ := client.GetProtocol(services[0].ID)

    // 执行服务 | Execute service
    result, _ := client.Execute(protocol, map[string]interface{}{
        "action": "get_menu",
    })

    fmt.Println(result)
}
```
</details>

<details>
<summary>🐍 Python</summary>

```python
from a2e import A2EClient

client = A2EClient("https://api.a2e-platform.com")

# 搜索服务 | Search services
services = client.search_services("奶茶店")

# 获取协议 | Get protocol
protocol = client.get_protocol(services[0].id)

# 执行服务 | Execute service
result = client.execute(protocol, {"action": "get_menu"})
print(result)
```
</details>

<details>
<summary>🟡 JavaScript / TypeScript</summary>

```typescript
import { A2EClient } from 'a2e-protocol';

const client = new A2EClient('https://api.a2e-platform.com');

// 搜索服务 | Search services
const services = await client.searchServices('奶茶店');

// 获取协议 | Get protocol
const protocol = await client.getProtocol(services[0].id);

// 执行服务 | Execute service
const result = await client.execute(protocol, { action: 'get_menu' });
console.log(result);
```
</details>

---

## 📋 协议规范 | Protocol Spec

A2E协议采用YAML/JSON格式描述服务，包含**8大核心模块**：

The A2E protocol uses YAML/JSON format to describe services, consisting of **8 core modules**:

| 模块 Module | 说明 Description |
|-------------|-----------------|
| `version` | 协议版本 Protocol version |
| `service` | 服务基本信息 Service metadata (id, name, type, provider) |
| `semantic` | 语义描述（供LLM理解）Semantic description for LLM comprehension |
| `authentication` | 认证方式 Authentication methods |
| `permissions` | 权限与费用说明 Permissions & pricing |
| `data_format` | 数据结构定义 Data structure definitions |
| `endpoints` | 可调用端点 Callable endpoints |
| `error_handling` | 错误码与处理策略 Error codes & retry strategies |

### 协议示例 | Protocol Example

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

📖 完整规范 Full Specification → [A2E Protocol Specification](spec/a2e-protocol-spec.md)

---

## SDK

| SDK | 状态 Status | 文档 Docs |
|-----|-------------|-----------|
| [Go SDK](sdk/go) | ✅ 可用 Available | [README](sdk/go/README.md) |
| [Python SDK](sdk/python) | ✅ 可用 Available | [README](sdk/python/README.md) |
| [JavaScript SDK](sdk/javascript) | ✅ 可用 Available | [README](sdk/javascript/README.md) |

---

## 📂 示例 | Examples

| 示例 Example | 说明 Description |
|-------------|-----------------|
| [AI Agent 接入示例](examples/ai-agent-demo) | 展示如何让AI Agent调用A2E服务 — How an AI Agent invokes A2E services |
| [服务提供商示例](examples/provider-demo) | 展示如何创建符合A2E协议的服务 — How to build an A2E-compliant service |

---

## 🏗️ 架构 | Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  AI Agent   │────▶│ A2E Platform │────▶│   Provider   │
│ (LLM-based) │◀────│   (Gateway)  │◀────│  (Services)  │
└─────────────┘     └──────────────┘     └──────────────┘
       │                   │                     │
       │    A2E Protocol   │    HTTP / REST      │
       └───────────────────┴─────────────────────┘
```

**工作流程 | Workflow:**

1. **发现 Discover** — AI Agent 通过语义搜索在平台发现可用服务
2. **理解 Understand** — 获取A2E协议文件，LLM解析语义描述理解服务能力
3. **认证 Authenticate** — 通过平台令牌完成身份验证
4. **执行 Execute** — AI Agent 构建请求并调用服务端点
5. **交易 Transact** — 涉及付费服务时，通过标准化订单流程完成支付

---

## 🌍 应用场景 | Use Cases

| 场景 Scenario | 描述 Description |
|--------------|-----------------|
| 🍵 餐饮外卖 Food Delivery | AI助手帮用户点奶茶、订餐 — AI orders milk tea & food for users |
| 🚗 出行服务 Transportation | AI助手帮用户打车、订票 — AI books rides & tickets |
| 🛒 购物消费 Shopping | AI助手帮用户比价、下单 — AI compares prices & places orders |
| 🏠 生活服务 Home Services | AI助手帮用户预约家政、维修 — AI books cleaning & repairs |

---

## 🤝 贡献 | Contributing

我们欢迎所有形式的贡献！ We welcome all forms of contributions!

- 🐛 [报告Bug Report Bugs](https://github.com/gulou69/AI-to-Everything/issues)
- 💡 [提出建议 Suggest Features](https://github.com/gulou69/AI-to-Everything/issues)
- 📖 改进文档 Improve Documentation
- 🔧 提交代码 Submit Code

请阅读 [贡献指南 Contributing Guide](CONTRIBUTING.md) 了解详情。

---

## 🗺️ Roadmap

- [x] v1.0 — 基础协议规范 Core protocol specification
- [ ] v1.1 — 流式响应支持 Streaming response support
- [ ] v1.2 — 多语言协议描述 Multi-language protocol descriptions
- [ ] v2.0 — 智能合约集成 Smart contract integration

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).

---

<p align="center">
  <sub>Built with ❤️ for the AI-powered future</sub>
</p>
