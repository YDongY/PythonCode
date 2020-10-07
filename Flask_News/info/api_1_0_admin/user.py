from . import admin
from flask import render_template, g, redirect, current_app, session, request
from info.utils.commons import login_required
from info.models import User
from datetime import datetime, time, timedelta
from info import constants


@admin.route("/admin/user_count")
@login_required
def user_count():
    if not g.user:
        return redirect("/admin/login")
    else:
        if not session.get("is_admin"):
            return render_template("admin/login.html")

    #  todo:查询总人数,除了管理员的其他所有用户
    total_count = 0

    try:
        total_count = User.query.filter(User.is_admin == 0).count()
    except Exception as e:
        current_app.logger.error(e)

    # todo:查询月新增数，用户注册时间大于本月的起始时间：xxxx-xx-xx 00:00:00
    mon_count = 0
    # 当前时间:2019-04-25 22:40:07.307013
    # 年-----------now.year：2019
    # 月-----------now.month：4
    # 日-----------now.day:25
    now = datetime.now()
    try:
        mon_begin = '%d-%02d-01' % (now.year, now.month)  # 2019-04-01 

        mon_begin_date = datetime.strptime(mon_begin, '%Y-%m-%d')  # 2019-04-01 00:00:00

        mon_count = User.query.filter(User.is_admin == 0, User.create_time >= mon_begin_date).count()

    except Exception as e:
        current_app.logger.error(e)

    # todo:查询日新增数,用户注册时间大于当天的的时间：xxxx-xx-xx 00:00:00

    day_count = 0

    try:
        day_begin = '%d-%02d-%02d' % (now.year, now.month, now.day)  # 2019-04-26

        day_begin_date = datetime.strptime(day_begin, '%Y-%m-%d')  # 2019-04-26 00:00:00

        day_count = User.query.filter(User.is_admin == 0, User.create_time >= day_begin_date).count()

    except Exception as e:
        current_app.logger.error(e)

    now_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')  # 2019-04-26 00:00:00

    # todo: 活动时间
    active_date = []
    # todo: 活动人数
    active_count = []

    for i in range(0, 31):
        try:

            begin_date = now_date - timedelta(days=i)

            end_date = now_date - timedelta(days=(i - 1))

            # todo:当天开始，过去30数天，每天的起始时间
            # todo:[2019-04-26 00:00:00,2019-04-25 00:00:00,2019-04-24 00:00:00.....]

            active_date.append(begin_date.strftime('%Y-%m-%d'))

            count = User.query.filter(User.is_admin == 0, User.last_login >= begin_date,
                                      User.last_login < end_date).count()
            # todo:过去30天每天登录的人数
            active_count.append(count)

        except Exception as e:
            current_app.logger.error(e)

    # todo:反转数据
    active_count.reverse()
    active_date.reverse()

    data = {
        "total_count": total_count,
        "mon_count": mon_count,
        "day_count": day_count,
        "active_date": active_date,
        "active_count": active_count
    }

    return render_template('admin/user_count.html', data=data)


@admin.route("/admin/user_list")
@login_required
def user_list():
    if not g.user:
        return redirect("/admin/login")
    else:
        if not session.get("is_admin"):
            return render_template("admin/login.html")
    page = request.args.get("p", 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    try:
        paginator = User.query.filter(User.is_admin == 0).paginate(page, constants.ADMIN_USER_INFO_MAX, False)
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/user_list.html", data=False, errmsg="查询异常")

    current_page = paginator.page
    total_page = paginator.pages
    items = paginator.items

    # 用户信息列表
    user_info_list = []
    for user in items:
        user_info_list.append(user.to_dict())

    data = {
        "user_info_list": user_info_list,
        "current_page": current_page,
        "total_page": total_page
    }
    return render_template("admin/user_list.html", data=data)
