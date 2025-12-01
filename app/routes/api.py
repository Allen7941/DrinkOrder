"""API 路由"""

from datetime import datetime

from flask import Blueprint, jsonify, request

from app import db
from app.models import Event, MenuItem, Order, Shop

api_bp = Blueprint("api", __name__)


# ==================== 飲料店 API ====================


@api_bp.route("/shops", methods=["GET"])
def get_shops():
    """取得所有飲料店"""
    shops = Shop.query.filter_by(is_active=True).all()
    return jsonify({"success": True, "data": [shop.to_dict() for shop in shops]})


@api_bp.route("/shops", methods=["POST"])
def create_shop():
    """新增飲料店"""
    data = request.get_json()

    if not data or not data.get("shop_name"):
        return jsonify({"success": False, "message": "店家名稱為必填"}), 400

    shop = Shop(
        shop_name=data["shop_name"],
        phone=data.get("phone"),
        address=data.get("address"),
    )

    db.session.add(shop)
    db.session.commit()

    return jsonify(
        {"success": True, "data": shop.to_dict(), "message": "飲料店新增成功"}
    ), 201


@api_bp.route("/shops/<shop_id>", methods=["PUT"])
def update_shop(shop_id):
    """更新飲料店"""
    shop = Shop.query.get_or_404(shop_id)
    data = request.get_json()

    if data.get("shop_name"):
        shop.shop_name = data["shop_name"]
    if "phone" in data:
        shop.phone = data["phone"]
    if "address" in data:
        shop.address = data["address"]
    if "is_active" in data:
        shop.is_active = data["is_active"]

    db.session.commit()

    return jsonify(
        {"success": True, "data": shop.to_dict(), "message": "飲料店更新成功"}
    )


@api_bp.route("/shops/<shop_id>", methods=["DELETE"])
def delete_shop(shop_id):
    """刪除飲料店 (軟刪除)"""
    shop = Shop.query.get_or_404(shop_id)
    shop.is_active = False
    db.session.commit()

    return jsonify({"success": True, "message": "飲料店已刪除"})


# ==================== 菜單 API ====================


@api_bp.route("/shops/<shop_id>/menu", methods=["GET"])
def get_menu(shop_id):
    """取得指定店家菜單"""
    items = MenuItem.query.filter_by(shop_id=shop_id, is_available=True).all()
    return jsonify({"success": True, "data": [item.to_dict() for item in items]})


@api_bp.route("/shops/<shop_id>/import-menu", methods=["POST"])
def import_menu(shop_id):
    """匯入菜單"""
    shop = Shop.query.get_or_404(shop_id)
    data = request.get_json()

    if not data or not data.get("items"):
        return jsonify({"success": False, "message": "請提供菜單資料"}), 400

    imported_count = 0
    for item_data in data["items"]:
        item = MenuItem(
            shop_id=shop_id,
            name=item_data["name"],
            category=item_data.get("category"),
            price_m=item_data.get("price_m"),
            price_l=item_data.get("price_l"),
            description=item_data.get("description"),
        )
        db.session.add(item)
        imported_count += 1

    db.session.commit()

    return jsonify({"success": True, "message": f"成功匯入 {imported_count} 個品項"})


# ==================== 團購活動 API ====================


@api_bp.route("/events", methods=["GET"])
def get_events():
    """取得團購活動列表"""
    status = request.args.get("status")

    query = Event.query
    if status:
        query = query.filter_by(status=status)

    events = query.order_by(Event.created_at.desc()).all()
    return jsonify({"success": True, "data": [event.to_dict() for event in events]})


@api_bp.route("/events", methods=["POST"])
def create_event():
    """建立新團購活動"""
    data = request.get_json()

    if not data or not data.get("shop_id"):
        return jsonify({"success": False, "message": "請選擇飲料店"}), 400

    shop = Shop.query.get_or_404(data["shop_id"])

    event = Event(
        shop_id=data["shop_id"],
        shop_name=shop.shop_name,
        created_by=data.get("created_by"),
        deadline=datetime.fromisoformat(data["deadline"])
        if data.get("deadline")
        else None,
        min_quantity=data.get("min_quantity", 0),
    )

    db.session.add(event)
    db.session.commit()

    return jsonify(
        {"success": True, "data": event.to_dict(), "message": "團購活動建立成功"}
    ), 201


@api_bp.route("/events/<event_id>", methods=["PUT"])
def update_event(event_id):
    """更新團購活動"""
    event = Event.query.get_or_404(event_id)
    data = request.get_json()

    if "status" in data:
        event.status = data["status"]
    if "deadline" in data:
        event.deadline = (
            datetime.fromisoformat(data["deadline"]) if data["deadline"] else None
        )

    db.session.commit()

    return jsonify(
        {"success": True, "data": event.to_dict(), "message": "團購活動更新成功"}
    )


@api_bp.route("/events/<event_id>/orders", methods=["GET"])
def get_event_orders(event_id):
    """取得團購活動的所有訂單"""
    event = Event.query.get_or_404(event_id)
    orders = Order.query.filter_by(event_id=event_id).all()

    # 計算統計資料
    total_cups = sum(order.quantity for order in orders)
    total_amount = sum(order.total_price or 0 for order in orders)

    # 品項統計
    items_count = {}
    for order in orders:
        key = f"{order.drink_name}-{order.size}-{order.sugar}-{order.ice}"
        items_count[key] = items_count.get(key, 0) + order.quantity

    return jsonify(
        {
            "success": True,
            "data": {
                "event_id": event_id,
                "shop_name": event.shop_name,
                "orders": [order.to_dict() for order in orders],
                "summary": {
                    "total_cups": total_cups,
                    "total_amount": total_amount,
                    "items_count": items_count,
                },
            },
        }
    )


# ==================== 訂單 API ====================


@api_bp.route("/orders", methods=["POST"])
def create_order():
    """新增訂單"""
    data = request.get_json()

    if not data or not data.get("customer_name") or not data.get("drink_name"):
        return jsonify({"success": False, "message": "訂購人姓名和飲料為必填"}), 400

    # 取得飲料資訊
    drink = None
    if data.get("drink_id"):
        drink = MenuItem.query.get(data["drink_id"])

    # 計算價格
    unit_price = 0
    if drink:
        unit_price = drink.price_l if data.get("size") == "L" else drink.price_m or 0

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

    return jsonify(
        {"success": True, "order_id": order.order_id, "message": "訂單已成功送出！"}
    ), 201


@api_bp.route("/orders", methods=["GET"])
def get_orders():
    """取得訂單列表"""
    event_id = request.args.get("event_id")
    date = request.args.get("date")
    customer_name = request.args.get("customer_name")

    query = Order.query

    if event_id:
        query = query.filter_by(event_id=event_id)
    if customer_name:
        query = query.filter(Order.customer_name.contains(customer_name))
    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        query = query.filter(db.func.date(Order.order_time) == date_obj.date())

    orders = query.order_by(Order.order_time.desc()).all()

    return jsonify({"success": True, "data": [order.to_dict() for order in orders]})


@api_bp.route("/orders/<order_id>", methods=["PUT"])
def update_order(order_id):
    """更新訂單狀態"""
    order = Order.query.get_or_404(order_id)
    data = request.get_json()

    if "status" in data:
        order.status = data["status"]

    db.session.commit()

    return jsonify(
        {"success": True, "data": order.to_dict(), "message": "訂單狀態更新成功"}
    )


@api_bp.route("/orders/export", methods=["GET"])
def export_orders():
    """匯出訂單 (CSV 格式)"""
    event_id = request.args.get("event_id")

    query = Order.query
    if event_id:
        query = query.filter_by(event_id=event_id)

    orders = query.order_by(Order.order_time).all()

    # 生成 CSV
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # 標題列
    writer.writerow(
        [
            "訂單編號",
            "訂購人",
            "部門",
            "飲料店",
            "飲料名稱",
            "杯型",
            "甜度",
            "冰塊",
            "加料",
            "數量",
            "單價",
            "總價",
            "備註",
            "狀態",
        ]
    )

    for order in orders:
        writer.writerow(
            [
                order.order_id,
                order.customer_name,
                order.department or "",
                order.shop_name or "",
                order.drink_name,
                order.size or "",
                order.sugar or "",
                order.ice or "",
                order.toppings or "",
                order.quantity,
                order.unit_price or 0,
                order.total_price or 0,
                order.note or "",
                order.status or "",
            ]
        )

    from flask import Response

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=orders.csv"},
    )
