from flask import Blueprint

passport = Blueprint('api_1_0_passport', __name__)

from . import views
