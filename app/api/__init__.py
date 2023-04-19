from flask import Blueprint

api = Blueprint('appi', __name__, url_prefix = '/api')

from . import auth_routes, ig_routes, shop_routes

