from flask import Blueprint

index = Blueprint('api_1_0_index', __name__)

from . import views
