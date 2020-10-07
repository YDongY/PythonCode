from flask import current_app, jsonify, render_template, g, abort, request
from info.utils.response_code import RET
from info.models import News, User, Comment, CommentLike
from info.utils.commons import login_required
from info import constants, db
from . import detail


@detail.route("/news/news_collect", methods=["POST"])
@login_required
# 收藏新新闻
def news_collect():
    if not g.user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    resp_dict = request.get_json()

    news_id = resp_dict.get("news_id")
    action = resp_dict.get("action")

    if not all([news_id, action]):
        return jsonify(errno=RET.DATAERR, errmsg="参数不足")

    if not action in ["collect", "cancel_collect"]:
        return jsonify(errno=RET.DATAERR, errmsg="操作类型错误")

    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    else:
        if not news:
            abort(404)

    if action == "collect":
        g.user.collection_news.append(news)
    elif action == "cancel_collect":
        g.user.collection_news.remove(news)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="提交失败")
    return jsonify(errno=RET.OK, errmsg="操作成功")


@detail.route("/news/news_comment", methods=["POST"])
@login_required
# 评论此条新闻
def news_comment():
    if not g.user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    resp_dict = request.get_json()

    news_id = resp_dict.get("news_id")
    content = resp_dict.get("comment")
    parent_id = resp_dict.get("parent_id")

    if not all([news_id, content]):
        return jsonify(errno=RET.DATAERR, errmsg="参数不足")

    # 查询此条新闻,让评论加1
    try:
        news = News.query.get(news_id)
        news.comments_count += 1
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="新闻查询异常")

    # 4.创建评论对象，设置属性
    comment = Comment()
    comment.user_id = g.user.id
    comment.content = content
    comment.news_id = news_id

    # 如果是回复评论
    if parent_id:
        comment.parent_id = parent_id

    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库保存异常")

    # 6.返回响应
    return jsonify(errno=RET.OK, errmsg="操作成功", data=comment.to_dict())


@detail.route("/news/news_comment_like", methods=["POST"])
@login_required
# 点赞
def news_comment_like():
    if not g.user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    resp_dict = request.get_json()

    comment_id = resp_dict.get("comment_id")
    action = resp_dict.get("action")
    news_id = resp_dict.get("news_id")

    if not all([comment_id, action, news_id]):
        return jsonify(errno=RET.DATAERR, errmsg="参数不足")

    if not action in ["add", "remove"]:
        return jsonify(errno=RET.DATAERR, errmsg="操作类型错误")

    # 查询点赞的评论
    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=" 数据库查询异常")
    if not comment:
        return jsonify(errno=RET.NODATA, errmsg="评论不存在")

    if action == "add":
        # 判断用户是否已经点过赞了
        comment_like = CommentLike.query.filter(CommentLike.comment_id == comment_id,
                                                CommentLike.user_id == g.user.id).first()
        if not comment_like:
            comment_like = CommentLike()
            comment_like.comment_id = comment_id
            comment_like.user_id = g.user.id
            db.session.add(comment_like)

            # 将点赞数量 +1
            comment.like_count += 1
    # 取消点赞
    else:
        # 判断是否点过赞
        comment_like = CommentLike.query.filter(CommentLike.comment_id == comment_id,
                                                CommentLike.user_id == g.user.id).first()
        if comment_like:
            db.session.delete(comment_like)

            # 将点赞数量-1操作
            comment.like_count -= 1
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存数据库失败")
    else:
        return jsonify(errno=RET.OK, errmsg="操作成功")


@detail.route("/news/detail/<int:news_id>", methods=["GET"])
@login_required
# 新闻详情页
def newsDetail(news_id):
    if not news_id:
        return jsonify(errno=RET.DATAERR, errmsg="参数错误")

    # 查询数据库，返回点击量前10的新闻数据
    try:
        click_news = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)
    else:
        click_news_list = []
        if not click_news:
            click_news_list = []
        else:
            for news in click_news:
                click_news_list.append(news.to_dict())

    # 查处此条新闻信息
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")
    else:
        if not news:
            abort(404)

    # 判断用户是否收藏过该新闻
    # 判断是否关注此用户
    is_collected = False
    is_attention = False
    if g.user:
        if news in g.user.collection_news:
            is_collected = True

        # 关联对象可以直接进行filter
        if news.user and news.user.followers.filter(User.id == g.user.id).count() > 0:
            is_attention = True

    # 查出此条新闻所有用户的评论
    try:
        comments = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")

    # 查询用户对当前新闻,哪些评论点过赞
    if g.user:
        # 获取评论的id
        comment_ids = [comment.id for comment in comments]

        # 获取用户点赞过的评论, 的所有点赞对象
        # CommentLike.comment_id.in_(comment_ids): 获取当前新闻的,评论的,所有点赞对象(有张三,李四,王五的点赞)
        # CommentLike.user_id == g.user.id :过滤出了,某个(比如张三)人的点赞对象
        commentLike = CommentLike.query.filter(CommentLike.comment_id.in_(comment_ids),
                                               CommentLike.user_id == g.user.id).all()
        commentlike_id = [comm_like.comment_id for comm_like in commentLike]

    comments_info = []
    if comments:
        for comment in comments:
            comment_dict = comment.to_dict()
            comment_dict["is_like"] = False
            if g.user and comment.id in commentlike_id:
                comment_dict["is_like"] = True
            comments_info.append(comment_dict)

    # # 查询新闻作者的信息
    # try:
    #     author = User.query.filter(User.id == news.user_id).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")

    # 新闻总篇数
    # news_count = 0
    # # 查询新闻作者
    # if news.user_id:
    #     # 查询该作者发布的所有的新闻
    #     try:
    #         news_count = News.query.filter(News.user_id == author.id).count()
    #     except Exception as e:
    #         current_app.logger.error(e)
    #         return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")

    data = {
        "user_info": g.user.to_dict() if g.user else None,
        "news": news.to_dict(),
        "comments_info_list": comments_info,
        "is_collected": is_collected,
        "is_attention": is_attention,
        "news_info": click_news_list,
    }

    return render_template("news/detail.html", data=data)
