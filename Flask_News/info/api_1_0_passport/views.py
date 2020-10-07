from . import passport
from flask import request, jsonify, current_app, render_template, make_response
from info.utils.response_code import RET
from info.tasks.tasks_sms import send_sms
from info.utils.captcha.captcha import captcha
from info import redis_store, constants
from info.models import User, db
from flask import session

from datetime import datetime
import random


# 获取图片验证码
@passport.route("/image_code/<image_code_id>")
def get_image_code(image_code_id):
    name, text, image_data = captcha.generate_captcha()

    try:
        redis_store.setex('image_code_%s' % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRE, text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存验证码图片失败")

    resp = make_response(image_data)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


# GET : 127.0.0.1:5000/sms_codes/<mobile>?image_code=xxx&image_code_id=xxx
@passport.route("/sms_code/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    '''获取短信验证码'''
    image_code = request.args.get('image_code')
    image_code_id = request.args.get('image_code_id')

    if not all([image_code, image_code_id]):
        return jsonify(errno=RET.DATAERR, errmsg="参数不足")

    try:
        code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取验证码失败")

    if not code:
        return jsonify(errno=RET.NODATA, errmsg="验证码过期")

    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    if code.decode('utf-8').lower() != image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="验证码错误")

    # 判断对于这个手机号的操作，在60s内有没有之前的记录，如果有，认为用户操作频繁
    try:
        send_flag = redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60s后重试")

    try:
        user = User.query.filter(User.mobile == mobile).first()
        print(user)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg="该手机号已注册")

    sms_code = "%06d" % random.randint(0, 999999)

    # 保存短信验证码,和发送验证码的号码
    try:
        redis_store.setex('sms_code_%s' % sms_code, constants.SMS_CODE_REDIS_EXPIRE, sms_code)
        redis_store.setex('sms_mobile_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")

    # todo:celery异步发送短信
    send_sms.delay(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRE / 60)], 1)

    # 发送成功
    return jsonify(errno=RET.OK, errmsg="发送成功")


# 注册
@passport.route('/passport/register', methods=['POST'])
def register():
    resp_dict = request.get_json()

    mobile = resp_dict.get("mobile")
    sms_code = resp_dict.get("sms_code")
    password = resp_dict.get("password")
    checked = resp_dict.get("check")

    if not all([mobile, sms_code, password, checked]):
        return jsonify(errno=RET.DATAERR, errmsg='数据不完整')

    if checked != "on":
        return jsonify(errno=RET.DATAERR, errmsg="未同意条款")

    if len(password) < 6:
        return jsonify(errno=RET.DATAERR, errmsg='密码少于六位')

    try:
        smsCode = redis_store.get("sms_code_%s" % sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询短信验证码异常")
    if not sms_code:
        return jsonify(error=RET.NODATA, errmsg="短信验证码过期")

    if sms_code != smsCode.decode('utf-8'):
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")

    try:
        user = User(mobile=mobile, nick_name=mobile)
        user.password = password
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据库异常")
    else:
        return jsonify(errno=RET.OK, errmsg="OK")


@passport.route('/passport/login', methods=["POST"])
def login():
    '''登录'''
    resp_dict = request.get_json()

    mobile = resp_dict.get("mobile")
    password = resp_dict.get("password")

    if not all([mobile, password]):
        return jsonify(errno=RET.DATAERR, errmsg="数据不完整")

    try:
        user = User.query.filter(User.mobile == mobile).first()
        user.last_login = datetime.now()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")
    else:
        if not user:
            return jsonify(errno=RET.NODATA, errmsg="该用户未注册")
        else:
            if not user.check_passowrd(password):
                return jsonify(errno=RET.PWDERR, errmsg="密码错误")
            else:
                session["user_id"] = user.id
                session["nick_name"] = user.nick_name
                session["mobile"] = user.mobile
                if user.is_admin:
                    session["is_admin"] = True
                return jsonify(errno=RET.OK, errmsg="OK")


@passport.route('/passport/logout', methods=["delete"])
def logout():
    '''退出'''
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")
