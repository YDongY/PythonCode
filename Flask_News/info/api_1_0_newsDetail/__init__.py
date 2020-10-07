from flask import Blueprint

detail = Blueprint("api_1_0_newsDetail", __name__)

from . import views
