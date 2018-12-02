from flask import Blueprint
hrequests = Blueprint('hrequests', __name__)
from . import views
