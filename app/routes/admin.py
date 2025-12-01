"""管理頁面路由"""

from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/shops")
def shops():
    """飲料店管理頁"""
    return render_template("admin/shops.html")


@admin_bp.route("/shops/<shop_id>/import-menu")
def import_menu_page(shop_id):
    """匯入菜單頁"""
    return render_template("admin/import_menu.html", shop_id=shop_id)


@admin_bp.route("/events")
def events():
    """團購活動管理頁"""
    return render_template("admin/events.html")


@admin_bp.route("/orders")
def orders():
    """訂單彙總頁"""
    return render_template("admin/orders.html")
