import unittest
from app.models import User
from app import create_app, db
from tests.TestBase import TestBase


class UserModelTestCase(TestBase):

    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_creation(self):
        # create test admin user
        admin = User(username="admin", email="olawolemoses@gmail.com", password="admin2016", is_admin=True)

        # create test non-admin user
        user = User(username="test_user", password="test2016", email='test@test.com')

        # save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.query.count(), 2)
