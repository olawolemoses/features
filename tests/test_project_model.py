import unittest
from app.models import Project
from app import create_app, db
from tests.TestBase import TestBase


class ProjectModelTestCase(TestBase):

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
