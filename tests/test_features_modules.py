import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Feature, Project, ProductArea, Client
from datetime import datetime

class FeaturesModuleTestCase(unittest.TestCase):
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

    def test_admin_list_features(self):

        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)
        db.session.commit()

        product_area = ProductArea(product_area="product_area A")
        db.session.add(product_area)

        project = Project(project_name="Project A")
        db.session.add(project)

        client = Client(client_name="Client A")
        db.session.add(client)
        db.session.commit()

        #feature
        feature1 = Feature(title="update feature",
                            description="update description ",
                            client_priority=1,
                            target_date=datetime.now(),
                            product_area_id=product_area.id,
                            client_id=client.id,
                            project_id=project.id,
                            user_id=admin.id
                        )
        db.session.add(feature1)
        db.session.commit()

        # login admin
        # login with the new account
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # check users list
        response = self.client.get(url_for('hrequests.index'))
        self.assertTrue(response.status_code == 200)

        #confirm the list of users in the page
        self.assertTrue(feature1.title in response.data)

        # post a new feature
        response = self.client.post(url_for('hrequests.create'), data={
                'title': 'Feature A',
                'description': 'Desctiption A',
                'product_area_id': product_area.id,
                'client_priority': 1,
                'target_date':datetime.now(),
                'client':client.id,
                'project':project.id,
                'user':admin.id,
            }, follow_redirects=True)
        self.assertTrue(re.search('Feature A', response.data))

        # view a edit feature page
        response = self.client.get(url_for('hrequests.edit', id=feature1.id))
        self.assertTrue(re.search('update feature', response.data))

        # view a edit role page
        response = self.client.post(url_for('hrequests.edit', id=feature1.id),  data={
                'title': 'Feature X',
                'description' : feature1.description,
                'client_priority' : feature1.client_priority,
                'target_date' : "03/03/2018",
                'product_area' : feature1.product_area_id,
                'client' : feature1.client_id,
                'project' : feature1.project_id,
                'user' : admin.id
            })
        self.assertTrue(302 == response.status_code)

        # delete requests page
        response = self.client.post(url_for('hrequests.delete'),  data={
                'request_id':  feature1.id,
            }, follow_redirects=True)
        self.assertTrue(re.search('You have successfully deleted the Feature Request', response.data))
