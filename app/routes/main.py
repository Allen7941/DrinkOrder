"""主要頁面路由"""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """首頁"""
    return render_template("index.html")


@main_bp.route("/menu")
def menu():
    """菜單頁"""
    return render_template("menu.html")


@main_bp.route("/order")
def order():
    """訂購頁"""
    return render_template("order.html")


@main_bp.route("/order/confirm")
def order_confirm():
    """訂單確認頁"""
    return render_template("confirm.html")
