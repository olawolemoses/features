import unittest
from app.models import User
from app import create_app, db
from flask_testing import TestCase

class TestBase(TestCase):
    def create_app(self):

        # pass in test configuration
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://iws_admin:iws2016*@localhost/hrequests-test'
        )
        return app

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
