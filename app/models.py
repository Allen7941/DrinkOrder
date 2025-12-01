"""SQLAlchemy 資料模型"""

import uuid
from datetime import datetime

from app import db


def generate_uuid():
    """生成 UUID"""
    return str(uuid.uuid4())[:8].upper()


class Shop(db.Model):
    """飲料店模型"""

    __tablename__ = "shops"

    shop_id = db.Column(db.String(20), primary_key=True)
    shop_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯
    menu_items = db.relationship("MenuItem", backref="shop", lazy="dynamic")
    events = db.relationship("Event", backref="shop", lazy="dynamic")

    def __init__(self, **kwargs):
        if "shop_id" not in kwargs:
            kwargs["shop_id"] = f"SHOP{generate_uuid()}"
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "shop_id": self.shop_id,
            "shop_name": self.shop_name,
            "phone": self.phone,
            "address": self.address,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class MenuItem(db.Model):
    """菜單品項模型"""

    __tablename__ = "menu_items"

    item_id = db.Column(db.String(20), primary_key=True)
    shop_id = db.Column(db.String(20), db.ForeignKey("shops.shop_id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # 茶類/咖啡/果汁/特調
    price_m = db.Column(db.Integer)
    price_l = db.Column(db.Integer)
    description = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)

    def __init__(self, **kwargs):
        if "item_id" not in kwargs:
            kwargs["item_id"] = f"ITEM{generate_uuid()}"
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "shop_id": self.shop_id,
            "name": self.name,
            "category": self.category,
            "price_m": self.price_m,
            "price_l": self.price_l,
            "description": self.description,
            "is_available": self.is_available,
        }


class Event(db.Model):
    """團購活動模型"""

    __tablename__ = "events"

    event_id = db.Column(db.String(30), primary_key=True)
    shop_id = db.Column(db.String(20), db.ForeignKey("shops.shop_id"), nullable=False)
    shop_name = db.Column(db.String(100))
    created_by = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    min_quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="進行中")  # 進行中/已截止/已完成
    total_orders = db.Column(db.Integer, default=0)
    total_amount = db.Column(db.Integer, default=0)

    # 關聯
    orders = db.relationship("Order", backref="event", lazy="dynamic")

    def __init__(self, **kwargs):
        if "event_id" not in kwargs:
            today = datetime.now().strftime("%Y%m%d")
            kwargs["event_id"] = f"EVT-{today}-{generate_uuid()}"
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "shop_id": self.shop_id,
            "shop_name": self.shop_name,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "min_quantity": self.min_quantity,
            "status": self.status,
            "total_orders": self.total_orders,
            "total_amount": self.total_amount,
        }


class Order(db.Model):
    """訂單模型"""

    __tablename__ = "orders"

    order_id = db.Column(db.String(30), primary_key=True)
    event_id = db.Column(db.String(30), db.ForeignKey("events.event_id"))
    order_time = db.Column(db.DateTime, default=datetime.utcnow)
    customer_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50))
    shop_id = db.Column(db.String(20))
    shop_name = db.Column(db.String(100))
    drink_name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(10))  # M/L
    sugar = db.Column(db.String(20))  # 正常/少糖/半糖/微糖/無糖
    ice = db.Column(db.String(20))  # 正常冰/少冰/微冰/去冰/熱飲
    toppings = db.Column(db.String(100))  # 以逗號分隔
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    note = db.Column(db.String(200))
    status = db.Column(db.String(20), default="待處理")  # 待處理/已訂購/已送達

    def __init__(self, **kwargs):
        if "order_id" not in kwargs:
            today = datetime.now().strftime("%Y%m%d")
            kwargs["order_id"] = f"ORD-{today}-{generate_uuid()}"
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "event_id": self.event_id,
            "order_time": self.order_time.isoformat() if self.order_time else None,
            "customer_name": self.customer_name,
            "department": self.department,
            "shop_id": self.shop_id,
            "shop_name": self.shop_name,
            "drink_name": self.drink_name,
            "size": self.size,
            "sugar": self.sugar,
            "ice": self.ice,
            "toppings": self.toppings,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "note": self.note,
            "status": self.status,
        }
