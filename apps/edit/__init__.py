from flask import Blueprint
edit_blueprint = Blueprint('edit_blueprint', __name__, template_folder='edit_templates', static_folder='edit_static')
from . import views
