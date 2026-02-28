"""
服务提供商 A2E 接入示例

演示奶茶店如何创建符合 A2E 协议的服务
"""

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import secrets

app = FastAPI(
    title="示例奶茶店 API",
    description="A2E协议服务提供商示例",
    version="1.0.0"
)

# ============ 数据模型 ============

class ProductOption(BaseModel):
    sugar: List[str] = ["全糖", "七分糖", "半糖", "三分糖", "无糖"]
    ice: List[str] = ["正常冰", "少冰", "去冰", "热"]


class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str
    category: str
    options: ProductOption


class OrderItemOptions(BaseModel):
    sugar: Optional[str] = "全糖"
    ice: Optional[str] = "正常冰"


class OrderItem(BaseModel):
    product_id: int
    quantity: int = 1
    options: Optional[OrderItemOptions] = None


class CreateOrderRequest(BaseModel):
    items: List[OrderItem]
    address: str
    phone: str
    note: Optional[str] = None


class OrderResponse(BaseModel):
    order_no: str
    total_amount: float
    status: str
    status_text: str
    payment_url: Optional[str] = None
    estimated_time: Optional[str] = None


# ============ 模拟数据 ============

MENU: List[Product] = [
    Product(
        id=1,
        name="招牌奶茶",
        price=12.00,
        description="经典招牌，香浓醇厚，使用优质红茶配合鲜奶",
        category="招牌系列",
        options=ProductOption()
    ),
    Product(
        id=2,
        name="芝士茉莉",
        price=18.00,
        description="茉莉花茶配芝士奶盖，清香与浓郁的完美结合",
        category="芝士系列",
        options=ProductOption(ice=["正常冰", "少冰", "去冰"])
    ),
    Product(
        id=3,
        name="杨枝甘露",
        price=22.00,
        description="芒果、西柚、椰奶的热带风情",
        category="鲜果系列",
        options=ProductOption(sugar=["全糖", "半糖"], ice=["正常冰", "少冰"])
    ),
    Product(
        id=4,
        name="多肉葡萄",
        price=20.00,
        description="新鲜葡萄果肉，酸甜可口",
        category="鲜果系列",
        options=ProductOption()
    ),
]

# 订单存储（模拟数据库）
ORDERS: Dict[str, dict] = {}


# ============ 工具函数 ============

def check_shop_open() -> bool:
    """检查店铺是否营业"""
    hour = datetime.now().hour
    return 9 <= hour < 21


def generate_order_no() -> str:
    """生成订单号"""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = secrets.token_hex(3).upper()
    return f"A2E{now}{random_part}"


def verify_consumer_token(token: str) -> dict:
    """
    验证 Consumer Token
    
    实际应用中需要：
    1. 调用 A2E 平台 API 验证 Token 有效性
    2. 获取 Token 关联的用户信息
    """
    if not token or not token.startswith("token_"):
        raise HTTPException(status_code=401, detail={
            "code": "INVALID_TOKEN",
            "message": "无效的用户Token"
        })
    
    # 模拟返回用户信息
    return {
        "user_id": "user_12345",
        "nickname": "张三"
    }


# ============ API 端点 ============

@app.get("/api/menu")
async def get_menu(category: Optional[str] = Query(None, description="按分类筛选")):
    """
    获取菜单
    
    A2E 协议端点: get_menu
    """
    menu = MENU
    
    if category:
        menu = [p for p in MENU if p.category == category]
    
    # 按分类组织
    categories: Dict[str, list] = {}
    for product in menu:
        if product.category not in categories:
            categories[product.category] = []
        categories[product.category].append(product.model_dump())
    
    return {
        "categories": [
            {"name": name, "items": items}
            for name, items in categories.items()
        ],
        "total_count": len(menu)
    }


@app.post("/api/orders", response_model=OrderResponse)
async def create_order(
    request: CreateOrderRequest,
    x_consumer_token: str = Header(..., description="A2E平台用户Token")
):
    """
    创建订单
    
    A2E 协议端点: create_order
    需要用户授权: user_phone, user_address
    需要支付: 是
    """
    # 1. 验证 Token
    user_info = verify_consumer_token(x_consumer_token)
    
    # 2. 检查营业时间
    if not check_shop_open():
        raise HTTPException(status_code=400, detail={
            "code": "SHOP_CLOSED",
            "message": "店铺已打烊，营业时间为 9:00-21:00"
        })
    
    # 3. 验证商品
    product_map = {p.id: p for p in MENU}
    total_amount = 0.0
    order_items = []
    
    for item in request.items:
        if item.product_id not in product_map:
            raise HTTPException(status_code=400, detail={
                "code": "INVALID_PRODUCT",
                "message": f"商品ID {item.product_id} 不存在"
            })
        
        product = product_map[item.product_id]
        
        # 验证选项
        if item.options:
            if item.options.sugar and item.options.sugar not in product.options.sugar:
                raise HTTPException(status_code=400, detail={
                    "code": "INVALID_OPTIONS",
                    "message": f"商品 {product.name} 不支持 {item.options.sugar} 选项"
                })
            if item.options.ice and item.options.ice not in product.options.ice:
                raise HTTPException(status_code=400, detail={
                    "code": "INVALID_OPTIONS",
                    "message": f"商品 {product.name} 不支持 {item.options.ice} 选项"
                })
        
        item_total = product.price * item.quantity
        total_amount += item_total
        order_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": item.quantity,
            "options": item.options.model_dump() if item.options else {},
            "unit_price": product.price,
            "total_price": item_total
        })
    
    # 4. 检查起送金额
    if total_amount < 10:
        raise HTTPException(status_code=400, detail={
            "code": "MIN_AMOUNT_NOT_MET",
            "message": f"订单金额 ¥{total_amount:.2f} 未达到起送标准 ¥10.00"
        })
    
    # 5. 创建订单
    order_no = generate_order_no()
    estimated_time = (datetime.now() + timedelta(minutes=30)).strftime("%H:%M")
    
    order = {
        "order_no": order_no,
        "user_id": user_info["user_id"],
        "items": order_items,
        "total_amount": total_amount,
        "address": request.address,
        "phone": request.phone,
        "note": request.note,
        "status": "pending_payment",
        "status_text": "待支付",
        "created_at": datetime.now().isoformat(),
        "estimated_time": estimated_time
    }
    
    ORDERS[order_no] = order
    
    return OrderResponse(
        order_no=order_no,
        total_amount=total_amount,
        status="pending_payment",
        status_text="待支付",
        payment_url=f"https://pay.a2e-platform.com/pay?order={order_no}&amount={total_amount}",
        estimated_time=f"预计 {estimated_time} 送达"
    )


@app.get("/api/orders/{order_no}", response_model=OrderResponse)
async def get_order_status(
    order_no: str,
    x_consumer_token: str = Header(..., description="A2E平台用户Token")
):
    """
    查询订单状态
    
    A2E 协议端点: get_order_status
    """
    # 1. 验证 Token
    user_info = verify_consumer_token(x_consumer_token)
    
    # 2. 查询订单
    if order_no not in ORDERS:
        raise HTTPException(status_code=404, detail={
            "code": "ORDER_NOT_FOUND",
            "message": f"订单 {order_no} 不存在"
        })
    
    order = ORDERS[order_no]
    
    # 3. 验证订单归属
    if order["user_id"] != user_info["user_id"]:
        raise HTTPException(status_code=403, detail={
            "code": "ACCESS_DENIED",
            "message": "无权访问此订单"
        })
    
    return OrderResponse(
        order_no=order["order_no"],
        total_amount=order["total_amount"],
        status=order["status"],
        status_text=order["status_text"],
        estimated_time=order.get("estimated_time")
    )


@app.get("/api/a2e/protocol")
async def get_protocol():
    """
    获取 A2E 协议定义
    
    AI Agent 可以通过此端点获取服务的完整协议信息
    """
    return {
        "version": "1.0.0",
        "service": {
            "id": "demo_tea_shop",
            "name": "示例奶茶店",
            "type": "food_delivery"
        },
        "semantic": {
            "description": "示例奶茶店，提供各类奶茶、果茶",
            "capabilities": ["在线点餐", "自定义口味", "外卖配送"]
        },
        "endpoints": [
            {"name": "get_menu", "path": "/api/menu", "method": "GET"},
            {"name": "create_order", "path": "/api/orders", "method": "POST"},
            {"name": "get_order_status", "path": "/api/orders/{order_no}", "method": "GET"}
        ]
    }


# ============ 健康检查 ============

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "shop_open": check_shop_open()}


# ============ 启动 ============

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print("  A2E Protocol - 服务提供商示例")
    print("  示例奶茶店 API 服务")
    print("=" * 50)
    print()
    print("API 文档: http://localhost:8000/docs")
    print("协议端点: http://localhost:8000/api/a2e/protocol")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
