import unittest

from flask_testing import TestCase

from app import create_app, db
from app.models import User, Client


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://root@localhost/hrequests-test'
        )
        db.init_app(app)
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = User(username="admin", email="olawolemoses@gmail.com", password="admin2016", is_admin=True)

        # create test non-admin user
        user = User(username="test_user", password="test2016", email='test@test.com')

        # save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestModels(TestBase):

    def test_user_model(self):
        """
        Test number of records in User table
        """
        self.assertEqual(User.query.count(), 2)

    def test_client_model(self):
        """
        Test number of records in Client table
        """

        # create test department
        clientA = Client(client_name="Client A")
        clientB = Client(client_name="Client B")
        clientC = Client(client_name="Client C")

        # save department to database
        db.session.add(clientA)
        db.session.add(clientB)
        db.session.add(clientC)
        db.session.commit()

        self.assertEqual(Client.query.count(), 3)

    def test_role_model(self):
        """
        Test number of records in Role table
        """

        # create test role
        role = Role(name="Admin", description="Admin to Site")

        # save role to database
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)

if __name__ == '__main__':
    unittest.main()
