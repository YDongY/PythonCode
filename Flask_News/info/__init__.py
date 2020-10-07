from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_session import Session
from info.utils.commons import ReConverter

import redis
import logging
import flask_whooshalchemyplus
from logging.handlers import RotatingFileHandler

# 数据库
db = SQLAlchemy()

# 创建redis链接对象
redis_store = None

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器，指明日志保存路径，每个日志文件的最大大小，保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def creat_app(config_name):
    app = Flask(__name__)

    # 获取配置信息
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)


    # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT,
                                    db=config_class.REDIS_DB)

    # 利用flask_session将session数据保存到redis数据库
    Session(app)

    # csrf防护
    CSRFProtect(app)

    # 设置请求钩子after_request,每次请求完成之后都会走该钩子修饰的方法
    @app.after_request
    def after_request(resp):
        csrf_token = generate_csrf()
        resp.set_cookie("csrf_token", csrf_token)
        return resp

    # 为flask添加自定义转换器
    app.url_map.converters["re"] = ReConverter

    # 导入蓝图
    from info import api_1_0_passport, api_1_0_index, api_1_0_newsDetail, api_1_0_user
    app.register_blueprint(api_1_0_passport.passport)
    app.register_blueprint(api_1_0_index.index)
    app.register_blueprint(api_1_0_newsDetail.detail)
    app.register_blueprint(api_1_0_user.user)

    from info import api_1_0_admin
    app.register_blueprint(api_1_0_admin.admin)

    return app
