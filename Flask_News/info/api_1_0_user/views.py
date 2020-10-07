from flask import current_app, g, render_template, jsonify, redirect, request
from . import user
from info.utils.commons import login_required
from info.utils import image_storage
from info.utils.response_code import RET
from info.models import User, News, Category
from info import db, constants
from sqlalchemy import and_
from info.utils.image_storage import storage


@user.route("/user/user_base_info", methods=["GET", "PUT"])
@login_required
# 用户基本信息
def user_base_info():
    if not g.user:
        return redirect("/")

    if request.method == "GET":
        data = {"user_info": g.user.to_dict()}
        return render_template("news/user_base_info.html", data=data)

    resp_dict = request.get_json()

    signature = resp_dict.get("signature") if resp_dict.get("signature") else None
    nick_name = resp_dict.get("nick_name")
    gender = resp_dict.get("gender")

    if not all([nick_name, gender]):
        return jsonify(errno=RET.DATAERR, errmsg="数据不完整")
    try:
        user = User.query.filter_by(nick_name=nick_name).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库失败")
    else:
        if user:
            return jsonify(errno=RET.DATAERR, errmsg="用户名已存在")

    user_id = g.user.id
    if signature:
        try:
            User.query.filter_by(id=user_id).update(
                {"nick_name": nick_name, "signature": signature, "gender": gender})
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="查询数据库失败")
    else:
        try:
            User.query.filter_by(id=user_id).update({"nick_name": nick_name, "gender": gender})
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="查询数据库失败")
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存数据库失败")
    else:
        return jsonify(errno=RET.OK, errmsg="OK")


@user.route("/user/user_pic_info", methods=["GET", "PUT"])
@login_required
# 用户头像设置，七牛云存储
def user_pic_info():
    if not g.user:
        return redirect("/")

    if request.method == "GET":
        data = {"user_info": g.user.to_dict()}
        return render_template("news/user_pic_info.html", data=data)

    pic_file = request.files.get("avatar")
    if not pic_file:
        return jsonify(errno=RET.NODATA, errmsg="未上传图片")

    pic_data = pic_file.read()

    try:
        pic_name = image_storage.storage(pic_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="上传失败")
    else:
        avatar_url = constants.QINIU_URL_DOMAIN + pic_name

    try:
        User.query.filter_by(id=g.user.id).update({"avatar_url": avatar_url})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片失败")
    else:
        data = {"avatar_url": avatar_url}
        return jsonify(errno=RET.OK, errmsg="Ok", data=data)


@user.route("/user/user_pass_info", methods=["GET", "PUT"])
@login_required
# 用户密码修改
def user_pass_info():
    if not g.user:
        return redirect("/")

    if request.method == "GET":
        data = {"user_info": g.user.to_dict()}
        return render_template("news/user_pass_info.html", data=data)

    resp_dict = request.get_json()

    old_password = resp_dict.get("old_password")
    new_password = resp_dict.get("new_password")
    new_password2 = resp_dict.get("new_password2")

    if not all([old_password, new_password, new_password2]):
        return jsonify(errno=RET.DATAERR, errmsg="参数不足")

    if len(old_password) < 6 or len(new_password) < 6 or len(new_password2) < 6:
        return jsonify(errno=RET.DATAERR, errmsg="密码长度少于六位")

    if new_password2 != new_password:
        return jsonify(errno=RET.PWDERR, errmsg="两次密码不一样")

    if not g.user.check_passowrd(old_password):
        return jsonify(errno=RET.PWDERR, errmsg="旧密码输入错误")

    try:
        user = User.query.filter_by(id=g.user.id).first()
        user.password = new_password
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库保存异常")
    else:
        return jsonify(errno=RET.OK, errmsg="Ok")


@user.route("/user/user_collection", methods=["GET"])
@login_required
# 用户新闻收藏
def user_collection():
    if not g.user:
        return redirect("/")

    page = request.args.get("p", 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    try:
        paginate = g.user.collection_news.paginate(page, constants.USER_COLLECTION_MAX_NEWS, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据失败")

    # 获取分页中的内容,总页数,当前页,当前页的所有对象
    total_page = paginate.pages
    current_page = paginate.page
    items = paginate.items

    news_list = []
    for news in items:
        news_list.append(news.to_dict())

    data = {
        "total_page": total_page,
        "current_page": current_page,
        "news_list": news_list
    }

    return render_template("news/user_collection.html", data=data)


@user.route("/user/user_follow", methods=["GET"])
@login_required
# 用户关注页显示
def user_follow():
    if not g.user:
        return redirect("/")

    page = request.args.get("p", 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    try:
        paginator = g.user.followed.paginate(page, constants.USER_COLLECTION_MAX_FOLLOW)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询失败")

    current_page = paginator.page
    total_page = paginator.pages
    items = paginator.items

    fans_user_data = []

    for user in items:
        fans_user_data.append(user.to_dict())

    data = {
        "current_page": current_page,
        "total_page": total_page,
        "fans_user_data": fans_user_data
    }

    return render_template("news/user_follow.html", data=data)


@user.route("/user/user_news_release", methods=["GET", "POST"])
@login_required
# 用户新闻发布
def user_news_release():
    if not g.user:
        return redirect("/")

    if request.method == "GET":

        # 获取所用分类
        try:
            categorys = Category.query.order_by(Category.id).all()
        except Exception as e:
            current_app.logger.error(e)
            return render_template("news/user_news_release.html", errmsg="数据库异常")
        category_info = []
        if categorys:
            for category in categorys:
                category_info.append(category)
        data = {
            "category_info": category_info,
        }
        return render_template("news/user_news_release.html", data=data)
    else:
        title = request.form.get("title")
        category_id = request.form.get("category_id")
        digest = request.form.get("digest")
        index_image = request.files.get("index_image")
        content = request.form.get("content")

        if not all([title, category_id, digest, content]):
            return jsonify(errno=RET.DATAERR, errmsg="参数不足")

        if index_image:
            try:
                image_data = index_image.read()
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.DATAERR, errmsg="图片读取失败")

            try:
                image_url = storage(image_data)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.THIRDERR, errmsg="图片上传失败")
            else:
                if image_url:
                    image_url = constants.QINIU_URL_DOMAIN + image_url

        try:
            news = News(title=title, category_id=category_id, digest=digest,
                        content=content, index_image_url=image_url,
                        user_id=g.user.id, status=1, source=g.user.nick_name)
            db.session.add(news)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="数据库异常")

        return jsonify(errno=RET.OK, errmsg="OK")


@user.route("/user/user_news_list", methods=["GET"])
@login_required
# 用户新闻列表
def user_news_list():
    if not user:
        return redirect("/")

    page = request.args.get("p", 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    try:
        paginator = News.query.order_by(News.create_time.desc()).filter(News.user_id == g.user.id).paginate(page,
                                                                                                            constants.USER_NEWS_MAX,
                                                                                                            False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")

    current_page = paginator.page
    total_page = paginator.pages

    news_info = []
    for news in paginator.items:
        news_info.append(news.to_dict())

    data = {
        "current_page": current_page,
        "total_page": total_page,
        "news_info": news_info
    }
    return render_template("news/user_news_list.html", data=data)


@user.route("/user/user_like", methods=["POST"])
@login_required
# 关注和取消关注用户
def user_like():
    if not g.user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    resp_dict = request.get_json()

    user_id = resp_dict.get("user_id")
    action = resp_dict.get("action")

    if not all([user_id, action]):
        return jsonify(errno=RET.DATAERR, errmsg="参数不完整")

    if not action in ["attention", "noattention"]:
        return jsonify(errno=RET.DATAERR, errmsg="参数类型错误")

    # 查询被关注用户
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")
    else:
        if not user:
            return jsonify(errno=RET.NODATA, errmsg="查询用户不存在")

    # 关注
    if action == 'attention':
        if user.followers.filter(User.id == g.user.id).count() > 0:
            return jsonify(errno=RET.DATAEXIST, errmsg="当前已关注")
        user.followers.append(g.user)
    # 取消关注
    else:
        if user.followers.filter(User.id == g.user.id).count() > 0:
            user.followers.remove(g.user)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="提交失败")
    return jsonify(errno=RET.OK, errmsg="操作成功")


@user.route("/user/user_info", methods=["GET"])
@login_required
# 用户主页信息
def user_info():
    if not g.user:
        return redirect("/")
    else:
        data = {
            "user_info": g.user.to_dict()
        }
        return render_template("news/user.html", data=data)
