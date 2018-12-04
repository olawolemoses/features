import unittest
from app.models import Role
from app import create_app, db
from tests.TestBase import TestBase


class RoleTestCase(TestBase):

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
