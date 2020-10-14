# __Time__ : 2020/10/14 下午3:18
# __Author__ : '__YDongY__'


from datetime import datetime
from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)

