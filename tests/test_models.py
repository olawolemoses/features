import unittest
from app.models import ProductArea, Project, Role, User, Client
from app import create_app, db
from tests.TestBase import TestBase


class ModelsTestCase(TestBase):

    def test_productarea_creation(self):
        # create test clients
        productarea1 = ProductArea(product_area="Product Area A")
        productarea2 = ProductArea(product_area="Product Area B")
        productarea3 = ProductArea(product_area="Product Area C")

        # save client to database
        db.session.add(productarea1)
        db.session.add(productarea2)
        db.session.add(productarea3)

        db.session.commit()

        self.assertEqual(ProductArea.query.count(), 3)

    def test_project_creation(self):
        # create test clients
        ProjectA = Project(project_name="Project A")
        ProjectB = Project(project_name="Project B")
        ProjectC = Project(project_name="Project C")

        # save client to database
        db.session.add(ProjectA)
        db.session.add(ProjectB)
        db.session.add(ProjectC)

        db.session.commit()

        self.assertEqual(Project.query.count(), 3)

    def test_role_creation(self):
        """
        Test number of records in Role table
        """
        # create test role
        role = Role(name="CEO", description="Run the whole company")

        # save role to database
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)

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

    def test_client_creation(self):
        # create test clients
        clientA = Client(client_name="Client A")
        clientB = Client(client_name="Client B")
        clientC = Client(client_name="Client C")

        # save client to database
        db.session.add(clientA)
        db.session.add(clientB)
        db.session.add(clientC)
        db.session.commit()

        self.assertEqual(Client.query.count(), 3)
