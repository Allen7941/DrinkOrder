"""訂單服務"""

from app import db
from app.models import Event, MenuItem, Order


class OrderService:
    """訂單相關業務邏輯"""

    @staticmethod
    def create_order(data):
        """建立新訂單"""
        # 取得飲料資訊
        drink = None
        if data.get("drink_id"):
            drink = MenuItem.query.get(data["drink_id"])

        # 計算價格
        unit_price = 0
        if drink:
            unit_price = (
                drink.price_l if data.get("size") == "L" else drink.price_m or 0
            )

        # 加料費用
        toppings = data.get("toppings", [])
        topping_price = len(toppings) * 10 if toppings else 0

        quantity = data.get("quantity", 1)
        total_price = (unit_price + topping_price) * quantity

        order = Order(
            event_id=data.get("event_id"),
            customer_name=data["customer_name"],
            department=data.get("department"),
            shop_id=data.get("shop_id"),
            shop_name=data.get("shop_name"),
            drink_name=data.get("drink_name") or (drink.name if drink else ""),
            size=data.get("size", "M"),
            sugar=data.get("sugar", "正常"),
            ice=data.get("ice", "正常冰"),
            toppings=",".join(toppings) if toppings else None,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            note=data.get("note"),
        )

        db.session.add(order)

        # 更新團購活動統計
        if data.get("event_id"):
            event = Event.query.get(data["event_id"])
            if event:
                event.total_orders = (
                    Order.query.filter_by(event_id=event.event_id).count() + 1
                )
                event.total_amount = (event.total_amount or 0) + total_price

        db.session.commit()
        return order

    @staticmethod
    def get_order_by_id(order_id):
        """根據 ID 取得訂單"""
        return Order.query.get(order_id)

    @staticmethod
    def get_orders_by_event(event_id):
        """取得團購活動的所有訂單"""
        return Order.query.filter_by(event_id=event_id).all()

    @staticmethod
    def update_order_status(order_id, status):
        """更新訂單狀態"""
        order = Order.query.get(order_id)
        if order:
            order.status = status
            db.session.commit()
            return order
        return None

    @staticmethod
    def get_order_summary(event_id):
        """取得訂單彙總"""
        orders = Order.query.filter_by(event_id=event_id).all()

        total_cups = sum(order.quantity for order in orders)
        total_amount = sum(order.total_price or 0 for order in orders)

        # 品項統計
        items_count = {}
        for order in orders:
            key = f"{order.drink_name}-{order.size}-{order.sugar}-{order.ice}"
            items_count[key] = items_count.get(key, 0) + order.quantity

        return {
            "total_cups": total_cups,
            "total_amount": total_amount,
            "items_count": items_count,
            "order_count": len(orders),
        }
