"""Настройки конфигурации для сред разработки, тестирования и производства.""" 
import os
from pathlib import Path


HERE = Path(__file__).parent
SQLITE_DEV = "sqlite:///" + str(HERE / "jwt_authentication_dev.db")
SQLITE_TEST = "sqlite:///" + str(HERE / "jwt_authentication_test.db")
SQLITE_PROD = "sqlite:///" + str(HERE / "jwt_authentication_prod.db")


class Config:
    """Базовая конфигурация.""" 
    SECRET_KEY = os.getenv("SECRET_KEY", "open sesame")
    BCRYPT_LOG_ROUND = 4
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGER = False
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    """Тестирование конфигурации."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = SQLITE_TEST


class DevelopmentConfig(Config):
    """Конфигурация разработки."""
    TOKEN_EXPIRE_MINUTES = 15
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_DEV)


class ProductionConfig(Config):
    """Производственная конфигурация.""" 
    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUND = 13
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_PROD)
    PRESERVE_CONTEXT_ON_EXCEPTION = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """Получить настройки конфигурации среды."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
