from flask import Blueprint

user = Blueprint("api_1_0_user", __name__)

from . import views
