from . import index
from flask import render_template
from flask import current_app, g, request, jsonify
from info.utils.commons import login_required
from info.models import News, Category
from info import constants, redis_store
from info.utils.response_code import RET


@index.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file("news/favicon.ico")


# 127.0.0.1:5000/newsList?page=1&cid=1&limit=10
@index.route('/newsList')
def newsList():
    page = request.args.get("page", 1)
    cid = request.args.get("cid")
    limit = request.args.get("limit", 10)

    try:
        page = int(page)
        limit = int(limit)
    except Exception as e:
        current_app.logger.error(e)
        page = 1
        limit = 10

    if cid:
        try:
            category = Category.query.get(cid)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="类型参数有误")
        else:
            if not category:
                cid = "1"

    # 判断分类编号是否不等于 1
    # 过滤条件的参数容器
    filters = []
    if cid != "1":
        filters.append(News.category_id == cid)

    filters.append(News.status == 0)

    # 3.根据条件查询数据
    try:

        paginator = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page=page,
                                                                                           per_page=limit,
                                                                                           error_out=False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")
    else:
        # 获取分页内容：总页数，当前页，当前页所有对象
        totalPage = paginator.pages
        currentPage = paginator.page
        items = paginator.items
        news_list = []

    for news in items:
        news_list.append(news.to_dict())

    return jsonify(errno=RET.OK, errmsg="OK", cid=cid, currentPage=currentPage, totalPage=totalPage,
                   news_list=news_list)


# @index.errorhandler(404)
# def handle_404_error(err):
#     return render_template('news/404.html')


@index.route('/', methods=['GET'])
@login_required
def index():
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

    # 导航条
    try:
        categorys = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
    else:
        category_list = []
        if not categorys:
            category_list = []
        else:
            for category in categorys:
                category_list.append(category.to_dict())

    data = {
        "user_info": g.user.to_dict() if g.user else None,
        "news_info": click_news_list,
        "category_info": category_list,
    }

    return render_template('news/index.html', data=data)
