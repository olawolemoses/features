from flask import Blueprint
productareas = Blueprint('productareas', __name__)
from . import views
