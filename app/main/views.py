from datetime import datetime
from flask import render_template, session, redirect, url_for, abort
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Log

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html',name=session.get('name'),
                                    known=session.get('known', False),
                                    current_time=datetime.utcnow())

@main.context_processor
def inject_logs():
    logs = Log.query.all()
    print "logs: ", logs
    return dict(logs=logs)
