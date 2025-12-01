"""Flask 應用程式初始化"""

import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """應用程式工廠函數"""
    app = Flask(__name__)

    # 載入設定
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    from app.config import config

    app.config.from_object(config[config_name])

    # 初始化擴展
    db.init_app(app)
    migrate.init_app(app, db)

    # 註冊藍圖
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp
    from app.routes.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # 建立資料庫表格
    with app.app_context():
        db.create_all()

    return app


# 為 WSGI 伺服器 (Gunicorn) 提供 app 實例
# 開發時使用 `flask run`，會自動呼叫 create_app()
# 生產環境使用 `gunicorn app:app`，會使用這個預先建立的實例
app = create_app()
