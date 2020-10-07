from flask import Blueprint

admin = Blueprint("api_1_0_admin", __name__)

from . import login, index, user, news
