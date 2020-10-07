from . import admin
from flask import render_template, g, redirect, current_app, session, request, jsonify, abort
from info.utils.commons import login_required
from info.models import Category, News
from sqlalchemy import or_
from info.utils.response_code import RET
from info import db, constants
from info.utils.image_storage import storage


@admin.route("/admin/news_review_detail", methods=["GET", "POST"])
@login_required
# 新闻审核
def news_review_detail():
    if not g.user:
        return redirect("/admin/login")
    else:
        if not session.get("is_admin"):
            return redirect("/admin/login")
    if request.method == "GET":
        id = request.args.get("id")
        if not id:
            abort(404)
        try:
            id = int(id)
        except Exception as e:
            current_app.logger.error(e)
            return render_template("admin/news_review_detail.html", errmsg="参数类型错误")

        # 查询对应id的新闻信息
        try:
            news = News.query.get(id)
        except Exception as e:
            current_app.logger.error(e)
            return render_template("admin/news_review_detail.html", errmsg="数据库异常")
        else:
            if not news:
                return render_template("admin/news_review_detail.html", errmsg="数据库查询异常")

        data = {
            "news_info": news.to_dict(),

        }
        return render_template("admin/news_review_detail.html", data=data)

    if request.method == "POST":
        resp_dict = request.get_json()

        news_id = resp_dict.get("news_id")
        action = resp_dict.get("action")
        reason = resp_dict.get("reason")

        if not all([news_id, action]):
            return jsonify(errno=RET.DATAERR, errmsg="参数不足")

        if action not in ["accept", "reject"]:
            return jsonify(errno=RET.DATAERR, errmsg="参数类型错误")

        try:
            news = News.query.get(news_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")

        if action == "accept":
            news.status = 0
        else:
            news.reason = reason
            news.status = -1
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="数据库保存异常")
        return jsonify(errno=RET.OK, errmsg=RET.OK)


@admin.route("/admin/news_review")
@login_required
# 新闻审核列表页面
def news_review():
    if not g.user:
        return redirect("/admin/login")
    else:
        if not session.get("is_admin"):
            return redirect("/admin/login")

    page = request.args.get("p", 1)

    keywords = request.args.get('key', "")

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    filters = [News.status != 0]

    if keywords:
        filters.append(News.title.contains(keywords))

    try:
        paginator = News.query.order_by(News.create_time.desc()).filter(*filters).paginate(page, 1, False)
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/news_review.html", errmsg="查询异常")

    news_info = []
    current_page = paginator.page
    total_page = paginator.pages

    for news in paginator.items:
        news_info.append(news.to_dict())

    data = {
        "news_info": news_info,
        "current_page": current_page,
        "total_page": total_page
    }

    return render_template("admin/news_review.html", data=data)


@admin.route("/admin/news_edit")
@login_required
# 新闻编辑
def news_edit():
    if not g.user:
        return redirect("/admin/login")
    else:
        if not session.get("is_admin"):
            return redirect("/admin/login")

    page = request.args.get("p", 1)
    keywords = request.args.get('key', "")

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    try:
        filters = []
        if keywords:
            filters.append(News.title.contains(keywords))
        # todo:按照id排序
        paginator = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,
                                                                                           constants.ADMIN_NEWS_INFO_MAX,
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

    return render_template("admin/news_edit.html", data=data)


@admin.route("/admin/news_edit_detail", methods=["GET", "POST"])
@login_required
# 新闻编辑列表页面
def news_edit_detail():
    if not g.user:
        return redirect("/admin/login")
    else:
        if not session.get("is_admin"):
            return redirect("/admin/login")

    if request.method == "GET":
        id = request.args.get("id")
        if not id:
            abort(404)
        try:
            id = int(id)
        except Exception as e:
            current_app.logger.error(e)
            return render_template("admin/news_edit_detail.html", errmsg="参数类型错误")

        # 查询对应id的新闻信息
        try:
            news = News.query.get(id)
        except Exception as e:
            current_app.logger.error(e)
            return render_template("admin/news_edit_detail.html", errmsg="数据库异常")
        else:
            if not news:
                return render_template("admin/news_edit_detail.html", errmsg="数据库查询异常")

        # 查询所有分类
        try:
            categorys = Category.query.order_by().all()
        except Exception as e:
            current_app.logger.error(e)
            return render_template("admin/news_edit_detail.html", errmsg="数据库异常")
        category_info = []
        if categorys:
            for category in categorys:
                category_info.append(category.to_dict())

        data = {
            "news_info": news.to_dict(),
            "category_info": category_info
        }
        return render_template("admin/news_edit_detail.html", data=data)

    if request.method == "POST":

        news_id = request.form.get("news_id")
        news_title = request.form.get("news_title")
        news_digest = request.form.get("news_digest")
        news_content = request.form.get("news_content")
        news_image = request.files.get("news_image")
        news_category_id = request.form.get("news_category_id")

        if not all([news_title, news_digest, news_content, news_category_id]):
            return jsonify(errno=RET.PARAMERR, errmsg="参数有误")

        # resp_dict = request.get_json()
        #
        # news_title = resp_dict.get("news_title", "")
        # news_category_id = resp_dict.get("news_category_id", "")
        # news_image_url = resp_dict.get("news_image_url", "")
        # news_digest = resp_dict.get("news_digest", "")
        # news_content = resp_dict.get("news_content", "")

        if not news_id:
            abort(404)
        try:
            news_id = int(news_id)
            news_category_id = int(news_category_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DATAERR, errmsg="参数类型错误")

        try:
            news = News.query.get(news_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")
        else:
            if not news:
                return jsonify(errno=RET.NODATA, errmsg="没有此新闻")

        # 获取图片
        if news_image:
            try:
                news_image = news_image.read()
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.PARAMERR, errmsg="参数有误")

            try:
                image_url = storage(news_image)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.THIRDERR, errmsg="上传失败")
            else:
                if image_url:
                    news_image = constants.QINIU_URL_DOMAIN + image_url
                    news.index_image_url = news_image

        news.title = news_title
        news.category_id = news_category_id
        news.digest = news_digest
        news.content = news_content

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="保存数据库异常")
        return jsonify(errno=RET.OK, errmsg="OK")


@admin.route("/admin/news_type")
@login_required
# 显示类型页
def news_type():
    if not g.user:
        return redirect("/admin/login")
    else:
        if not session.get("is_admin"):
            return redirect("/admin/login")

    category_info = []
    try:
        categorys = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if categorys:
            for category in categorys:
                category_info.append(category.to_dict())

    data = {
        "category_info": category_info
    }

    return render_template("admin/news_type.html", data=data)


@admin.route("/admin/add_category", methods=["POST"])
@login_required
# 类型添加和修改
def news_type_add():
    if not g.user:
        return redirect("/admin/login")
    else:
        if not session.get("is_admin"):
            return redirect("/admin/login")

    resp_dict = request.get_json()

    id = resp_dict.get("id")
    name = resp_dict.get("name")

    if not all([name]):
        return jsonify(errno=RET.DATAERR, errmsg="参数不足")

    if id:
        try:
            id = int(id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DATAERR, errmsg="参数内容错误")

        try:
            category = Category.query.get(id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")

        try:
            category.name = name
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="数据库保存异常")
    else:
        category = Category(name=name)
        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="保存异常")

    return jsonify(errno=RET.OK, errmsg="OK")
