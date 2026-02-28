# 服务提供商接入示例

本示例展示服务提供商（如奶茶店）如何创建符合A2E协议的服务。

## 场景说明

模拟一家奶茶店接入A2E平台，提供在线点餐服务。

## 目录结构

```
provider-demo/
├── README.md
├── protocol.yaml        # A2E Protocol definition / A2E协议定义
└── python/              # Python (FastAPI) implementation / Python实现示例
    ├── main.py
    └── requirements.txt
```

## A2E 协议定义

创建 `protocol.yaml` 文件定义服务：

```yaml
a2e_protocol:
  version: "1.0.0"
  
  service:
    id: "my_tea_shop"
    name: "我的奶茶店"
    type: "food_delivery"
    provider:
      id: "provider_001"
      name: "我的奶茶店"
      certification: "personal"
  
  semantic:
    description: "一家提供各类奶茶、果茶的小店，支持自定义糖度和温度"
    keywords: ["奶茶", "果茶", "饮品"]
    capabilities:
      - "在线浏览菜单"
      - "自定义口味"
      - "外卖配送"
    constraints:
      - "配送范围：3公里内"
      - "营业时间：9:00-21:00"
  
  authentication:
    required: true
    methods:
      - type: "platform_token"
        description: "使用A2E平台Token认证"
  
  permissions:
    required:
      - name: "user_phone"
        description: "联系电话用于配送"
      - name: "user_address"
        description: "配送地址"
  
  endpoints:
    - name: "get_menu"
      path: "/api/menu"
      method: "GET"
      description: "获取菜单列表"
      requires_payment: false
      
    - name: "create_order"
      path: "/api/orders"
      method: "POST"
      description: "创建订单"
      requires_payment: true
```

## 实现服务接口

### Python (FastAPI)

```python
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 菜单数据
MENU = [
    {
        "id": 1,
        "name": "招牌奶茶",
        "price": 12.00,
        "description": "经典招牌",
        "options": {
            "sugar": ["全糖", "七分糖", "半糖", "无糖"],
            "ice": ["正常冰", "少冰", "去冰", "热"]
        }
    }
]

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    options: dict = {}

class CreateOrderRequest(BaseModel):
    items: List[OrderItem]
    address: str
    phone: str
    note: Optional[str] = None

@app.get("/api/menu")
async def get_menu():
    """获取菜单"""
    return {"menu": MENU}

@app.post("/api/orders")
async def create_order(
    request: CreateOrderRequest,
    x_consumer_token: str = Header(...)
):
    """创建订单"""
    # 验证Token (实际需调用A2E平台验证)
    if not x_consumer_token:
        raise HTTPException(401, "Unauthorized")
    
    # 计算金额
    total = sum(
        MENU[item.product_id - 1]["price"] * item.quantity
        for item in request.items
    )
    
    # 创建订单 (实际需保存到数据库)
    order = {
        "order_no": "ORD20260208001",
        "total_amount": total,
        "status": "pending_payment",
        "payment_url": f"https://pay.a2e-platform.com/pay?order=ORD20260208001"
    }
    
    return order
```

## 注册服务到平台

1. 登录A2E平台设计师后台
2. 创建新的工作流
3. 上传 `protocol.yaml` 或通过可视化设计器配置
4. 配置外部API地址
5. 提交审核

## 接入清单

- [ ] 定义A2E协议文档
- [ ] 实现API接口
- [ ] 部署服务并确保可访问
- [ ] 在A2E平台注册服务
- [ ] 提交审核
- [ ] 测试完整流程
