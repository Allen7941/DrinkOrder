"""飲料店服務"""

from app import db
from app.models import MenuItem, Shop


class ShopService:
    """飲料店相關業務邏輯"""

    @staticmethod
    def get_all_active_shops():
        """取得所有啟用的飲料店"""
        return Shop.query.filter_by(is_active=True).all()

    @staticmethod
    def get_shop_by_id(shop_id):
        """根據 ID 取得飲料店"""
        return Shop.query.get(shop_id)

    @staticmethod
    def create_shop(shop_name, phone=None, address=None):
        """建立新飲料店"""
        shop = Shop(shop_name=shop_name, phone=phone, address=address)
        db.session.add(shop)
        db.session.commit()
        return shop

    @staticmethod
    def update_shop(shop_id, **kwargs):
        """更新飲料店資訊"""
        shop = Shop.query.get(shop_id)
        if not shop:
            return None

        for key, value in kwargs.items():
            if hasattr(shop, key):
                setattr(shop, key, value)

        db.session.commit()
        return shop

    @staticmethod
    def delete_shop(shop_id):
        """軟刪除飲料店"""
        shop = Shop.query.get(shop_id)
        if shop:
            shop.is_active = False
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_menu_items(shop_id):
        """取得店家的菜單品項"""
        return MenuItem.query.filter_by(shop_id=shop_id, is_available=True).all()

    @staticmethod
    def import_menu(shop_id, items_data):
        """匯入菜單"""
        imported_items = []
        for item_data in items_data:
            item = MenuItem(
                shop_id=shop_id,
                name=item_data["name"],
                category=item_data.get("category"),
                price_m=item_data.get("price_m"),
                price_l=item_data.get("price_l"),
                description=item_data.get("description"),
            )
            db.session.add(item)
            imported_items.append(item)

        db.session.commit()
        return imported_items
