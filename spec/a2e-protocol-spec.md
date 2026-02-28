# A2E Protocol Specification v1.0.0

## 概述

A2E (Agent-to-EveryThing) 协议是一套专为AI Agent设计的服务接口描述标准。本文档定义了协议的完整规范。

---

## 1. 协议结构

A2E协议文档采用YAML或JSON格式，包含以下顶层字段：

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `a2e_protocol` | object | 是 | 协议根对象 |

### 1.1 完整结构

```yaml
a2e_protocol:
  version: string              # 协议版本
  service: ServiceInfo         # 服务信息
  semantic: SemanticInfo       # 语义描述
  authentication: AuthInfo     # 认证配置
  permissions: PermissionInfo  # 权限要求
  data_format: DataFormat      # 数据格式
  endpoints: Endpoint[]        # 接口列表
  error_handling: ErrorHandling # 错误处理
```

---

## 2. 字段定义

### 2.1 版本 (version)

```yaml
version: "1.0.0"  # 遵循语义化版本
```

### 2.2 服务信息 (service)

描述服务的基本信息。

```yaml
service:
  id: string           # 服务唯一标识
  name: string         # 服务名称（人类可读）
  type: string         # 服务类型
  provider:            # 服务提供商
    id: string
    name: string
    certification: string  # none/personal/enterprise/gold
```

**服务类型枚举**：
- `food_delivery` - 餐饮外卖
- `transportation` - 出行服务
- `shopping` - 购物消费
- `life_service` - 生活服务
- `entertainment` - 娱乐休闲
- `finance` - 金融服务
- `custom` - 自定义类型

### 2.3 语义描述 (semantic)

为AI提供理解服务的语义信息。

```yaml
semantic:
  description: string      # 自然语言描述（给AI看的）
  keywords: string[]       # 关键词标签
  capabilities: string[]   # 服务能力列表
  constraints: string[]    # 约束条件
  examples: Example[]      # 使用示例
```

**示例**：

```yaml
semantic:
  description: |
    这是一家位于上海的奶茶店，提供各类奶茶、果茶饮品。
    支持自定义糖度（全糖、七分糖、半糖、三分糖、无糖）和
    温度（正常冰、少冰、去冰、温、热）。
    提供5公里内外卖配送服务。
  keywords:
    - 奶茶
    - 果茶
    - 饮品
    - 外卖
    - 配送
  capabilities:
    - 在线浏览菜单
    - 自定义口味下单
    - 外卖配送
    - 在线支付
  constraints:
    - 配送范围：5公里内
    - 营业时间：10:00-22:00
    - 起送金额：15元
  examples:
    - query: "我想点一杯少糖去冰的招牌奶茶"
      action: "create_order"
      params:
        item: "招牌奶茶"
        sugar: "少糖"
        ice: "去冰"
```

### 2.4 认证配置 (authentication)

定义访问服务所需的认证方式。

```yaml
authentication:
  required: boolean        # 是否需要认证
  methods:                 # 支持的认证方式
    - type: string         # platform_token/oauth2/api_key
      description: string  # 认证说明
      endpoint: string     # 认证接口地址
```

**认证类型**：

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `platform_token` | 平台统一认证 | 推荐，用户通过平台认证 |
| `oauth2` | OAuth 2.0 | 第三方授权 |
| `api_key` | API密钥 | 简单场景 |

### 2.5 权限要求 (permissions)

定义执行服务所需的用户权限。

```yaml
permissions:
  required:               # 必需权限
    - name: string        # 权限名称
      description: string # 权限说明（给用户看）
      endpoint: string    # 获取该信息的接口
  optional:               # 可选权限
    - name: string
      description: string
      endpoint: string
```

**预定义权限**：

| 权限名 | 说明 |
|--------|------|
| `user_phone` | 用户手机号 |
| `user_address` | 用户地址 |
| `user_location` | 用户实时位置 |
| `user_payment` | 支付能力 |
| `user_profile` | 用户基本信息 |

### 2.6 数据格式 (data_format)

定义数据交换格式。

```yaml
data_format:
  input:
    type: string          # json/form/xml
    encoding: string      # utf-8
  output:
    type: string
    encoding: string
    human_readable: boolean  # 输出是否适合直接展示给用户
```

### 2.7 接口列表 (endpoints)

定义服务提供的所有接口。

```yaml
endpoints:
  - name: string            # 接口名称（英文标识）
    path: string            # 接口路径
    method: string          # HTTP方法
    description: string     # 接口描述（给AI看）
    requires_payment: boolean  # 是否涉及支付
    input_schema: JSONSchema   # 输入参数Schema
    output_schema: JSONSchema  # 输出参数Schema
    output_description: string # 输出说明（给AI理解）
    examples: Example[]        # 调用示例
```

**接口示例**：

```yaml
endpoints:
  - name: "get_menu"
    path: "/execute/get_menu"
    method: "POST"
    description: "获取店铺完整菜单，包含所有可售商品及其价格、可选配置"
    requires_payment: false
    input_schema:
      type: object
      properties:
        category:
          type: string
          description: "分类筛选（可选）"
    output_schema:
      type: object
      properties:
        menu:
          type: array
          items:
            type: object
            properties:
              id: { type: integer }
              name: { type: string }
              price: { type: number }
              description: { type: string }
              options:
                type: object
                properties:
                  sugar: { type: array, items: { type: string } }
                  ice: { type: array, items: { type: string } }
    output_description: |
      返回商品列表，每个商品包含：
      - id: 商品ID，下单时使用
      - name: 商品名称
      - price: 价格（元）
      - description: 商品描述
      - options: 可选配置，如糖度、温度等
    examples:
      - request: {}
        response:
          menu:
            - id: 1
              name: "招牌奶茶"
              price: 15.00
              description: "经典招牌，香浓醇厚"
              options:
                sugar: ["全糖", "七分糖", "半糖", "三分糖", "无糖"]
                ice: ["正常冰", "少冰", "去冰", "温", "热"]

  - name: "create_order"
    path: "/execute/create_order"
    method: "POST"
    description: "创建订单，需要用户已授权手机号和地址"
    requires_payment: true
    input_schema:
      type: object
      required: ["items", "address", "phone"]
      properties:
        items:
          type: array
          description: "购买的商品列表"
          items:
            type: object
            required: ["product_id", "quantity"]
            properties:
              product_id: { type: integer }
              quantity: { type: integer }
              options: { type: object }
        address:
          type: string
          description: "配送地址"
        phone:
          type: string
          description: "联系电话"
        note:
          type: string
          description: "备注（可选）"
    output_schema:
      type: object
      properties:
        order_no: { type: string }
        total_amount: { type: number }
        payment_url: { type: string }
    output_description: |
      创建订单成功后返回：
      - order_no: 订单号
      - total_amount: 待支付金额
      - payment_url: 支付链接，用户需要完成支付
```

### 2.8 错误处理 (error_handling)

定义服务可能返回的错误及处理建议。

```yaml
error_handling:
  codes:
    - code: string          # 错误码
      description: string   # 错误描述
      suggestion: string    # 处理建议（给AI提示如何应对）
```

**示例**：

```yaml
error_handling:
  codes:
    - code: "SERVICE_CLOSED"
      description: "店铺已打烊"
      suggestion: "告知用户当前不在营业时间，询问是否需要预约明天的订单"
    - code: "OUT_OF_STOCK"
      description: "商品已售罄"
      suggestion: "告知用户该商品已售完，推荐其他类似商品"
    - code: "OUT_OF_RANGE"
      description: "超出配送范围"
      suggestion: "告知用户地址超出配送范围，询问是否更换地址"
    - code: "MIN_AMOUNT_NOT_MET"
      description: "未达到起送金额"
      suggestion: "告知用户当前金额不足起送标准，建议添加更多商品"
```

---

## 3. 完整示例

```yaml
a2e_protocol:
  version: "1.0.0"
  
  service:
    id: "tea_shop_001"
    name: "茶语时光奶茶店"
    type: "food_delivery"
    provider:
      id: "provider_001"
      name: "茶语时光餐饮有限公司"
      certification: "enterprise"
  
  semantic:
    description: |
      茶语时光是一家精品奶茶店，提供各类手工现制奶茶、果茶、
      芝士茶等饮品。所有饮品支持自定义糖度和温度。
      提供上海市区5公里内外卖配送服务，平均配送时间30分钟。
    keywords:
      - 奶茶
      - 果茶
      - 芝士茶
      - 饮品
      - 外卖
      - 手工现制
    capabilities:
      - 在线浏览完整菜单
      - 自定义糖度（全糖/七分/半糖/三分/无糖）
      - 自定义温度（正常冰/少冰/去冰/温/热）
      - 添加小料（珍珠/椰果/仙草等）
      - 外卖配送服务
      - 在线支付
    constraints:
      - 配送范围：5公里内
      - 营业时间：10:00-22:00
      - 起送金额：15元
      - 配送费：满30免配送费，否则3元
  
  authentication:
    required: true
    methods:
      - type: "platform_token"
        description: "通过A2E平台获取用户身份Token"
        endpoint: "/api/v1/open/platform/get_user_token"
  
  permissions:
    required:
      - name: "user_phone"
        description: "需要您的手机号用于配送员联系"
        endpoint: "/api/v1/open/platform/get_user_phone"
      - name: "user_address"
        description: "需要您的地址用于外卖配送"
        endpoint: "/api/v1/open/platform/get_user_address"
    optional:
      - name: "user_profile"
        description: "获取昵称用于会员积分"
        endpoint: "/api/v1/open/platform/get_user_profile"
  
  data_format:
    input:
      type: "json"
      encoding: "utf-8"
    output:
      type: "json"
      encoding: "utf-8"
      human_readable: true
  
  endpoints:
    - name: "get_menu"
      path: "/execute/get_menu"
      method: "POST"
      description: "获取店铺完整菜单"
      requires_payment: false
      input_schema:
        type: object
        properties: {}
      output_schema:
        type: object
        properties:
          categories:
            type: array
            items:
              type: object
              properties:
                name: { type: string }
                items: { type: array }
      output_description: "返回分类整理的菜单列表"
    
    - name: "create_order"
      path: "/execute/create_order"
      method: "POST"
      description: "创建订单并获取支付链接"
      requires_payment: true
      input_schema:
        type: object
        required: ["items", "address", "phone"]
        properties:
          items:
            type: array
            items:
              type: object
              properties:
                product_id: { type: integer }
                quantity: { type: integer }
                options: { type: object }
          address: { type: string }
          phone: { type: string }
      output_schema:
        type: object
        properties:
          order_no: { type: string }
          total_amount: { type: number }
          payment_url: { type: string }
      output_description: "返回订单信息和支付链接"
    
    - name: "get_order_status"
      path: "/execute/get_order_status"
      method: "POST"
      description: "查询订单状态"
      requires_payment: false
      input_schema:
        type: object
        required: ["order_no"]
        properties:
          order_no: { type: string }
      output_schema:
        type: object
        properties:
          status: { type: string }
          status_text: { type: string }
          estimated_time: { type: string }
      output_description: "返回订单当前状态和预计送达时间"
  
  error_handling:
    codes:
      - code: "SERVICE_CLOSED"
        description: "店铺已打烊"
        suggestion: "告知用户当前不在营业时间（10:00-22:00）"
      - code: "OUT_OF_STOCK"
        description: "商品已售罄"
        suggestion: "推荐其他类似饮品"
      - code: "OUT_OF_RANGE"
        description: "超出配送范围"
        suggestion: "告知用户地址超出5公里配送范围"
```

---

## 4. API调用流程

### 4.1 服务发现流程

```
AI Agent                    A2E Platform
    │                           │
    │  1. 搜索服务               │
    │  POST /services/search    │
    │  {"keyword": "奶茶"}       │
    │─────────────────────────>│
    │                           │
    │  2. 返回服务列表           │
    │  [服务1, 服务2, ...]      │
    │<─────────────────────────│
    │                           │
    │  3. 获取服务协议           │
    │  GET /services/{id}/protocol
    │─────────────────────────>│
    │                           │
    │  4. 返回A2E协议文档         │
    │<─────────────────────────│
```

### 4.2 服务调用流程

```
AI Agent                    A2E Platform                 Provider
    │                           │                           │
    │  1. 请求用户认证           │                           │
    │─────────────────────────>│                           │
    │  2. 返回Consumer Token    │                           │
    │<─────────────────────────│                           │
    │                           │                           │
    │  3. 执行工作流             │                           │
    │  POST /workflows/{id}/execute                        │
    │  {consumer_token, input}  │                           │
    │─────────────────────────>│  4. 调用Provider接口       │
    │                           │─────────────────────────>│
    │                           │  5. 返回结果              │
    │                           │<─────────────────────────│
    │  6. 返回执行结果           │                           │
    │<─────────────────────────│                           │
```

---

## 5. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-02-08 | 初始版本 |

---

## 6. 附录

### 6.1 JSON Schema

协议中的Schema定义遵循 [JSON Schema Draft-07](https://json-schema.org/draft-07/schema) 规范。

### 6.2 术语表

| 术语 | 定义 |
|------|------|
| AI Agent | 用户的AI助手，如ChatGPT |
| Consumer | 通过AI调用服务的终端用户 |
| Provider | 服务提供商 |
| Consumer Token | 终端用户的身份凭证 |
| Endpoint | 服务接口 |
