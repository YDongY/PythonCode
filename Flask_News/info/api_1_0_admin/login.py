from . import admin
from flask import request, current_app, jsonify, render_template, redirect, url_for, session
from info.utils.response_code import RET
from info.models import User


@admin.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        user_id = session.get("user_id", None)
        is_admin = session.get("is_admin", False)
        if user_id and is_admin:
            return redirect("/admin")
        return render_template('admin/login.html')

    username = request.form.get('username')
    passoword = request.form.get('password')

    if not all([username, passoword]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        user = User.query.filter(User.nick_name == username).first()
    except Exception as e:
        current_app.logger.error(e)
        return render_template('admin/login.html', errmsg="数据查询失败")

    if not user:
        return render_template('admin/login.html', errmsg="用户不存在")

    if not user.is_admin:
        return render_template('admin/login.html', errmsg="用户权限错误")

    if not user.check_passowrd(passoword):
        return render_template('admin/login.html', errmsg="用户密码错误")

    session["user_id"] = user.id
    session["nick_name"] = user.nick_name
    session["mobile"] = user.mobile
    if user.is_admin:
        session["is_admin"] = True

    return redirect("/admin")


@admin.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin/login")
