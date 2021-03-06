from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from wtf_tinymce import wtf_tinymce


from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = "You must be logged in to access this page."


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

csrf = CSRFProtect()

def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    csrf.init_app(app)

    bootstrap.init_app(app)

    mail.init_app(app)

    moment.init_app(app)

    db.init_app(app)

    login_manager.init_app(app)

    wtf_tinymce.init_app(app)

    # attach routes and custom error pages here

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .hrequests import hrequests as hrequests_blueprint
    app.register_blueprint(hrequests_blueprint, url_prefix='/hrequests')

    from .clients import clients as clients_blueprint
    app.register_blueprint(clients_blueprint, url_prefix='/clients')

    from .productareas import productareas as productareas_blueprint
    app.register_blueprint(productareas_blueprint, url_prefix='/productareas')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .projects import projects as projects_blueprint
    app.register_blueprint(projects_blueprint, url_prefix='/projects')

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500


    return app
