from app import db

from datetime import datetime

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(200))

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Integer, default=False)

    features = db.relationship("Feature", backref="user",  lazy='dynamic')
    logs = db.relationship("Log", backref="user",  lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('title', db.String(100), nullable=False)
    description = db.Column('description', db.Text,  nullable=False)
    client_priority = db.Column('client_priority', db.Integer)
    target_date = db.Column('target_date', db.DateTime)
    product_area_id = db.Column('product_area_id', db.Integer, db.ForeignKey('product_areas.id'), nullable=False)
    user_id = db.Column('user_id', db.Integer,  db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    logs = db.relationship("Log", backref="feature",  lazy='dynamic')

    def __init__(self, title, description, client_id, client_priority, target_date, product_area_id, user_id, project_id ):

        self.title = title
        self.description = description
        self.client_priority = client_priority
        self.target_date = target_date
        self.product_area_id = product_area_id
        self.user_id = user_id
        self.client_id = client_id
        self.project_id = project_id

    def __repr__(self):
        return '<Feature %r>' % self.title


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)

    features = db.relationship("Feature", backref="client",  lazy='dynamic')

    def __init__(self, client_name):
        self.client_name = client_name

    def __repr__(self):
        return '<Client %r>' % self.client_name


class Project(db.Model):

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)

    features = db.relationship("Feature", backref="project",  lazy='dynamic')

    def __init__(self, project_name):
        self.project_name = project_name

    def __repr__(self):
        return '<Project %r>' % self.project_name


class ProductArea(db.Model):

    __tablename__ = 'product_areas'

    id = db.Column(db.Integer, primary_key=True)
    product_area = db.Column(db.String(100), nullable=False)

    features = db.relationship("Feature", backref="product_area",  lazy='dynamic')


    def __init__(self, product_area):
        self.product_area = product_area

    def __repr__(self):
        return '<ProductArea %r>' % self.product_area

class Log(db.Model):

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer,  db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.Text)
    feature_id = db.Column('feature_id', db.Integer,  db.ForeignKey('features.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, user_id, feature_id, action, timestamp):
        self.user_id = user_id
        self.action = action
        self.feature_id = feature_id
        self.timestamp = timestamp

    def __repr__(self):
        return '<Log %r>' % self.user.username + ' ' + self.action \
                        + ' ' + self.feature.title + ' ' + unicode(self.timestamp)


from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
