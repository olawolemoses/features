from app import db

from datetime import datetime

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

from sqlalchemy.event import listen

# second solution
def insert_initial_values(*args, **kwargs):
    db.session.add(Client(client_name='Client A'))
    db.session.add(Client(client_name='Client B'))
    db.session.add(Client(client_name='Client C'))
    db.session.commit()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(200))

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

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

    @staticmethod
    def insert_clients():
        clients = {
            'client_name': 'Client A',
            'client_name': 'Client B',
            'client_name': 'Client C',

        }
        for c in clients:
            client = Client.query.filter_by(client_name=c.client_name).first()
            if client is None:
                client = Client(client_name=c.client_name)
            db.session.add(client)
        db.session.commit()

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
    username = db.Column('username', db.Text, nullable=False)
    action = db.Column(db.Text)
    feature = db.Column('feature', db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, username, feature, action, timestamp):
        self.username = username
        self.action = action
        self.feature = str(feature.id) + ' ' + feature.title
        self.timestamp = timestamp

    def __repr__(self):
        return '<Log %r>' % self.username + ' ' + self.action \
                        + ' ' + self.feature + ' ' + unicode(self.timestamp)


from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
