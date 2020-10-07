"""
    实体类 --
User        用户
News        新闻
Comment     评论
CommentLike 评论点赞
Category    新闻分类
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from info import db
from jieba.analyse.analyzer import ChineseAnalyzer


class BaseModel(object):
    """
        模型基类，为每个模型补充创建时间与更新时间
    """
    # 记录的创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 记录的更新时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


"""用户收藏表, 建立用户与其收藏新闻多对多的关系"""
tb_user_collection = db.Table(
    # 数据库表名
    "info_user_collection",
    # 数据库字段 ( 用户ID, 数据类型, 外键约束--info_user.id )
    db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True),
    # 数据库字段 ( 新闻ID, 数据类型, 外键约束--info_news.id )
    db.Column("news_id", db.Integer, db.ForeignKey("info_news.id"), primary_key=True),
    # 数据库字段 ( 创建时间, 数据类型, 默认当前时间 )
    db.Column("create_time", db.DateTime, default=datetime.now)
)
"""用户关注表，建立用户与其他用户的多对多关系"""
tb_user_follows = db.Table(
    # 数据库表名
    "info_user_fans",
    # 数据库字段 ( 当前用户ID, 数据类型, 外键约束--info_user.id )
    db.Column('follower_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True),
    # 数据库字段 ( 被关注用户ID, 数据类型, 外键约束--info_user.id )
    db.Column('followed_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True)
)


class User(BaseModel, db.Model):
    """
        用户信息
    BaseModel 继承 -- 实现创建时间和更新时间的补充
    db.Model 数据模型 -- 实体和数据库表名建立关系
    """
    # 数据库表名 -- 和当前类绑定
    __tablename__ = "info_user"
    """ORM建立  属性 = 数据库字段"""
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)  # 是否管理员
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(  # 性别
        db.Enum(
            "MAN",  # 男
            "WOMAN"  # 女
        ),
        default="MAN")  # 默认 男
    """db.relationship设置关系"""
    # 当前用户收藏的所有新闻 -- 关系 ( 新闻表, 中间表, 懒加载 )
    collection_news = db.relationship("News", secondary=tb_user_collection, lazy="dynamic")  # 用户收藏的新闻
    # 用户所有的粉丝, 添加了反向引用followed, 代表用户都关注了哪些人
    followers = db.relationship('User',  # 用户表
                                secondary=tb_user_follows,  # 中间表
                                primaryjoin=id == tb_user_follows.c.followed_id,  # 主要加入
                                secondaryjoin=id == tb_user_follows.c.follower_id,  # 次要加入
                                backref=db.backref('followed', lazy='dynamic'),  # 反向引用 ( 被关注表, 懒加载 )
                                lazy='dynamic')  # 懒加载
    # 用户针对新闻的评论信息 -- 关系 ( 评论表, 反向引用--用户表 )
    comments = db.relationship("Comment", backref="user")

    # 用户点过赞的评论信息 -- 关系 ( 评论表, 中间表, 懒加载 )
    like_comments = db.relationship("Comment", secondary="info_comment_like", lazy='dynamic')

    # 当前用户所发布的新闻 -- 关系 ( 新闻表, 反向引用--用户表, 懒加载 )
    news_list = db.relationship('News', backref='user', lazy='dynamic')

    # # 粉丝总数
    # followers_count = 0
    # # 新闻总数
    # news_count = 0

    # 装饰器 -- 读取
    @property
    def password(self):
        # 禁止读取
        raise AttributeError("当前属性不可读")

    # 装饰器 -- set
    @password.setter
    def password(self, value):
        """
            设置password
        :param value: 值
        :return:
        """
        # 获取加密后的值 -- 对原密码进行加密
        self.password_hash = generate_password_hash(value)

    def check_passowrd(self, password):
        """
            检测密码
        :param password: 密码
        :return:
        """
        # 解密后, 对比密码是否正确
        return check_password_hash(self.password_hash, password)

    #
    # # 装饰器 -- get
    # @property
    # def news_count(self):
    #     count = 0
    #     for _ in self.news_list:
    #         count += 1
    #     return count
    #
    # # 装饰器 -- get
    # @property
    # def followers_count(self):
    #     count = 0
    #     for _ in self.followers:
    #         count += 1
    #     return count

    def to_dict(self):
        """
            把对象数据转换为字典数据
        """
        # 封装字典
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "mobile": self.mobile,
            "avatar_url": self.avatar_url,
            "is_admin": self.is_admin,
            "signature": self.signature,
            "gender": self.gender,
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "followers_count": self.followers.count(),
            "news_count": self.news_list.count()
        }
        # 返回字典
        return resp_dict


class News(BaseModel, db.Model):
    """
        新闻
    BaseModel 继承 -- 实现创建时间和更新时间的补充
    db.Model 数据模型 -- 实体和数据库表名建立关系
    """

    # 全文检索字段
    __searchable__ = ['title']
    __analyzer__ = ChineseAnalyzer()

    # 数据库表名 -- 和当前类绑定
    __tablename__ = "info_news"
    """ORM建立  属性 = 数据库字段"""
    id = db.Column(db.Integer, primary_key=True)  # 新闻编号
    title = db.Column(db.String(256), nullable=False)  # 新闻标题
    source = db.Column(db.String(64), nullable=False)  # 新闻来源
    digest = db.Column(db.String(512), nullable=False)  # 新闻摘要
    content = db.Column(db.Text, nullable=False)  # 新闻内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    comments_count = db.Column(db.Integer, default=0)  # 评论量
    index_image_url = db.Column(db.String(256), default='')  # 新闻列表图片路径
    category_id = db.Column(db.Integer, db.ForeignKey("info_category.id"))  # 新闻分类
    user_id = db.Column(db.Integer, db.ForeignKey("info_user.id"))  # 当前新闻的作者id
    status = db.Column(db.Integer, default=0)  # 当前新闻状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过
    reason = db.Column(db.String(256))  # 未通过原因，status = -1 的时候使用

    # 当前新闻的所有评论 -- 关系 ( 评论, 懒加载 )
    comments = db.relationship("Comment", lazy="dynamic")

    def to_dict(self):
        """
            把对象数据转换为字典数据
        """
        # 封装字典
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "content": self.content,
            "clicks": self.clicks,
            "category_id": self.category_id,
            "comments_count": self.comments_count,
            "index_image_url": self.index_image_url,
            "category": self.category.to_dict(),
            "status": self.status,
            "reason": self.reason,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "author": self.user.to_dict() if self.user else None
        }
        # 返回字典
        return resp_dict

    def to_review_dict(self):
        """
            需要把新闻分类也一同封装
        :return:
        """
        resp_dict = self.to_dict()
        resp_dict["category"] = self.category
        # 返回字典
        return resp_dict


class Comment(BaseModel, db.Model):
    """
        评论
    BaseModel 继承 -- 实现创建时间和更新时间的补充
    db.Model 数据模型 -- 实体和数据库表名建立关系
    """
    # 数据库表名 -- 和当前类绑定
    __tablename__ = "info_comment"
    """ORM建立  属性 = 数据库字段"""
    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    user_id = db.Column(db.Integer, db.ForeignKey("info_user.id"), nullable=False)  # 用户id
    news_id = db.Column(db.Integer, db.ForeignKey("info_news.id"), nullable=False)  # 新闻id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    parent_id = db.Column(db.Integer, db.ForeignKey("info_comment.id"))  # 父评论id
    parent = db.relationship("Comment", remote_side=[id])  # 自关联
    like_count = db.Column(db.Integer, default=0)  # 点赞条数

    def to_dict(self):
        """
            把对象数据转换为字典数据
        """
        # 封装字典
        resp_dict = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "parent": self.parent.to_dict() if self.parent else None,
            "user": User.query.get(self.user_id).to_dict(),
            "news_id": self.news_id,
            "like_count": self.like_count
        }
        # 返回字典
        return resp_dict


class CommentLike(BaseModel, db.Model):
    """
        评论点赞
    BaseModel 继承 -- 实现创建时间和更新时间的补充
    db.Model 数据模型 -- 实体和数据库表名建立关系
    """
    # 数据库表名 -- 和当前类绑定
    __tablename__ = "info_comment_like"
    """ORM建立  属性 = 数据库字段"""
    comment_id = db.Column("comment_id", db.Integer, db.ForeignKey("info_comment.id"), primary_key=True)  # 评论编号
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True)  # 用户编号


class Category(BaseModel, db.Model):
    """
        新闻分类
    BaseModel 继承 -- 实现创建时间和更新时间的补充
    db.Model 数据模型 -- 实体和数据库表名建立关系
    """
    # 数据库表名 -- 和当前类绑定
    __tablename__ = "info_category"
    """ORM建立  属性 = 数据库字段"""
    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    # 当前新闻分类的具体新闻 -- 关系 ( 新闻表, 反向引用--新闻表中的新闻分类, 懒加载 )
    news_list = db.relationship('News', backref='category', lazy='dynamic')

    def to_dict(self):
        """
            把对象数据转换为字典数据
        """
        # 封装字典
        resp_dict = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "name": self.name,
        }
        # 返回字典
        return resp_dict
