"""路由模組"""

from app.routes.admin import admin_bp
from app.routes.api import api_bp
from app.routes.main import main_bp

__all__ = ["main_bp", "api_bp", "admin_bp"]
