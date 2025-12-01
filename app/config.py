"""應用程式設定檔"""

import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基礎設定"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """開發環境設定"""

    DEBUG = True
    # 本地開發使用 SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(
        os.path.dirname(basedir), "instance", "drink_order.db"
    )


class ProductionConfig(Config):
    """正式環境設定"""

    DEBUG = False
    # 正式環境使用 PostgreSQL (Zeabur 自動注入)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # 處理 Heroku/Zeabur 的 postgres:// URL 格式
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )


class TestingConfig(Config):
    """測試環境設定"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
