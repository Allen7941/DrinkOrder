"""團購活動服務"""

from datetime import datetime

from app import db
from app.models import Event, Shop


class EventService:
    """團購活動相關業務邏輯"""

    @staticmethod
    def create_event(shop_id, created_by=None, deadline=None, min_quantity=0):
        """建立新團購活動"""
        shop = Shop.query.get(shop_id)
        if not shop:
            return None

        event = Event(
            shop_id=shop_id,
            shop_name=shop.shop_name,
            created_by=created_by,
            deadline=deadline,
            min_quantity=min_quantity,
        )

        db.session.add(event)
        db.session.commit()
        return event

    @staticmethod
    def get_event_by_id(event_id):
        """根據 ID 取得團購活動"""
        return Event.query.get(event_id)

    @staticmethod
    def get_active_events():
        """取得進行中的團購活動"""
        return (
            Event.query.filter_by(status="進行中")
            .order_by(Event.created_at.desc())
            .all()
        )

    @staticmethod
    def get_all_events():
        """取得所有團購活動"""
        return Event.query.order_by(Event.created_at.desc()).all()

    @staticmethod
    def update_event_status(event_id, status):
        """更新團購活動狀態"""
        event = Event.query.get(event_id)
        if event:
            event.status = status
            db.session.commit()
            return event
        return None

    @staticmethod
    def close_event(event_id):
        """關閉團購活動"""
        return EventService.update_event_status(event_id, "已截止")

    @staticmethod
    def complete_event(event_id):
        """完成團購活動"""
        return EventService.update_event_status(event_id, "已完成")

    @staticmethod
    def check_expired_events():
        """檢查並更新過期的團購活動"""
        now = datetime.utcnow()
        expired_events = Event.query.filter(
            Event.status == "進行中", Event.deadline < now
        ).all()

        for event in expired_events:
            event.status = "已截止"

        if expired_events:
            db.session.commit()

        return len(expired_events)
