from flask import Blueprint
edit_blueprint = Blueprint('edit_blueprint', __name__, template_folder='templates', static_folder='static')
from . import views
