import redis
import os


class Config(object):
    """配置信息"""
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # mysql
    DB_NAME = os.environ.get("DB_NAME")
    DB_HOST = os.environ.get("DB_HOST")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_PORT = os.environ.get("DB_PORT")

    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_DB_HOST = os.environ.get("REDIS_DB_HOST")
    REDIS_DB_PORT = os.environ.get("REDIS_DB_PORT")
    REDIS_DB_NUM = os.environ.get("REDIS_DB_NUM")

    REDIS_HOST = f'{REDIS_DB_HOST}'
    REDIS_PORT = REDIS_DB_PORT
    REDIS_DB = REDIS_DB_NUM

    # flask-session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    SESSION_USE_SIGNER = True  # 对cookie中的session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位：秒


class DevelopmentConfig(Config):
    """开发模式"""
    DEBUG = True


class ProductConfig(Config):
    """生产环境配置信息"""
    pass


class TestConfig(object):
    """测试模式配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductConfig,
    'test': TestConfig
}
