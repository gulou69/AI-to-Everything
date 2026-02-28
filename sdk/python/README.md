# A2E Python SDK

A2E协议的官方Python SDK。

## 安装

```bash
pip install a2e-protocol
```

## 快速开始

```python
from a2e import A2EClient

# 创建客户端
client = A2EClient(
    base_url="https://api.a2e-platform.com",
    app_id="your_app_id",
    app_secret="your_app_secret"
)

# 搜索服务
services = client.search_services(keyword="奶茶", page=1, size=10)
print(f"找到 {len(services.list)} 个服务")

# 获取服务协议
protocol = client.get_protocol(services.list[0].id)
print(f"服务: {protocol.service.name}")
print(f"描述: {protocol.semantic.description}")

# 执行服务
result = client.execute(
    service_id=services.list[0].id,
    endpoint="get_menu",
    consumer_token="user_token_xxx",
    input_data={}
)
print(f"执行结果: {result.output}")
```

## 异步使用

```python
import asyncio
from a2e import AsyncA2EClient

async def main():
    client = AsyncA2EClient(base_url="https://api.a2e-platform.com")
    
    # 异步搜索
    services = await client.search_services(keyword="奶茶")
    
    # 异步执行
    result = await client.execute(
        service_id=services.list[0].id,
        endpoint="get_menu",
        consumer_token="token",
        input_data={}
    )
    
    print(result.output)

asyncio.run(main())
```

## API文档

### Client

```python
from a2e import A2EClient

client = A2EClient(
    base_url="https://api.a2e-platform.com",  # API地址
    app_id="your_app_id",                      # AppID（可选）
    app_secret="your_app_secret",              # AppSecret（可选）
    timeout=30                                  # 超时时间（秒）
)
```

### 搜索服务

```python
result = client.search_services(
    keyword="奶茶",           # 搜索关键词
    service_type="food_delivery",  # 服务类型（可选）
    location=(31.2304, 121.4737),  # 位置（可选）
    page=1,
    size=10
)
```

### 获取服务协议

```python
protocol = client.get_protocol(service_id)
```

### 执行服务

```python
result = client.execute(
    service_id="service_001",
    endpoint="get_menu",
    consumer_token="token_xxx",
    input_data={}
)
```

### 获取用户Token

```python
auth = client.get_consumer_token(
    auth_type="wechat",
    auth_code="wechat_auth_code"
)
print(auth.consumer_token)
```

## 错误处理

```python
from a2e import A2EError

try:
    result = client.execute(...)
except A2EError as e:
    print(f"API错误: {e.code} - {e.message}")
```

## License

Apache License 2.0
