import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Project

class ProjectTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_list_projects(self):

        # create 3  non-admin user
        project1 = Project(project_name="Project A")
        db.session.add(project1)
        project2 =Project(project_name="Project B")
        db.session.add(project2)
        project3 = Project(project_name="Project C")
        db.session.add(project3)

        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        db.session.commit()

        # login admin
        # login with the new account
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # check users list
        response = self.client.get(url_for('projects.index'))
        self.assertTrue(response.status_code == 200)

        #confirm the list of users in the page
        self.assertTrue(project1.project_name in response.data)
        self.assertTrue(project2.project_name in response.data)
        self.assertTrue(project3.project_name in response.data)

    def test_admin_add_project(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)
        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # post a new role
        response = self.client.post(url_for('projects.create'), data={
                'project_name': 'Project A',
            }, follow_redirects=True)


        self.assertTrue(re.search('Project A', response.data))

    def test_admin_edit_project(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        project = Project(project_name="Project A")
        db.session.add(project)

        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # view a edit role page
        response = self.client.get(url_for('projects.edit', id=project.id))
        self.assertTrue(re.search('Project A', response.data))

        # view a edit role page
        response = self.client.post(url_for('projects.edit', id=project.id),  data={
                'project_name': 'Project B'
            }, follow_redirects=True)


        self.assertTrue(re.search('Project B', response.data))

    def test_admin_delete_project(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        project = Project(project_name="Project A")
        db.session.add(project)

        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # view a edit role page
        response = self.client.post(url_for('projects.delete'),  data={
                'project_id':  project.id,
            }, follow_redirects=True)
        self.assertTrue(re.search('You have successfully deleted the project', response.data))
