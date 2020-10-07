from . import admin
from flask import render_template, g, session, redirect
from info.utils.commons import login_required


@admin.route("/admin", methods=["GET"])
@login_required
def index():
    if not g.user:
        return render_template("admin/login.html")
    else:
        if not session.get("is_admin"):
            return render_template("admin/login.html")

    data = {
        "user_info": g.user.to_dict()
    }
    return render_template("admin/index.html", data=data)
