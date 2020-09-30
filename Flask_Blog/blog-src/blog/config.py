# __Time__ : 2020/9/30 下午10:17
# __Author__ : '__YDongY__'


class Config(object):
    SECRET_KEY = 'ac061ec67d73b7bef81d476dbde0627c'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # SECRET_KEY = os.environ.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

    # 邮箱配置
    # 发送者邮箱的服务地址
    MAIL_SERVER = "smtp.qq.com"

    # 非加密25(qq邮箱不支持) ,加密：(TLS,587)/(SSL,465)
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = "1140068769@qq.com"
    MAIL_PASSWORD = "自己的"
    MAIL_DEFAULT_SENDER = "1140068769@qq.com"
    # MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
