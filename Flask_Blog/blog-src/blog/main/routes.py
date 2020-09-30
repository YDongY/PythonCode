# __Time__ : 2020/9/30 下午9:35
# __Author__ : '__YDongY__'

from flask import render_template, request, Blueprint
from blog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.create_time.desc()).paginate(page=page, per_page=2)  # 分页，每页两个
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
