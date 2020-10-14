# __Time__ : 2020/10/14 下午3:17
# __Author__ : '__YDongY__'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
